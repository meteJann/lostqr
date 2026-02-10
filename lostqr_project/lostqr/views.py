from .forms import ProfileForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Profile
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages



def home_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            return redirect('qrview', profile_id=profile.id)
    return render(request, "lostqr/home.html")

# Login View
def login_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            return redirect('qrview', profile_id=profile.id)
        else:
            return redirect('userhome')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            profile = Profile.objects.filter(user=user).first()
            if profile:
                return redirect('qrview', profile_id=profile.id)
            else:
                return redirect('userhome')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı. Lütfen bilgilerinizi kontrol edin.")
    else:
        form = AuthenticationForm()

    return render(request, 'lostqr/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız. Tekrar bekleriz!")
    return redirect('login')


# Create User
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('userhome')

    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        if not u_name or not p_word:
            messages.error(request, "Lütfen tüm alanları doldurun.")
            return render(request, 'lostqr/signup.html')

        if User.objects.filter(username=u_name).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
            return render(request, 'lostqr/signup.html')

        try:
            user = User.objects.create_user(username=u_name, password=p_word)
            login(request, user) # Kayıt sonrası otomatik giriş
            return redirect('userhome')
        except Exception as e:
            print(f"Hata oluştu: {e}")
            messages.error(request, "Kayıt sırasında bir hata oluştu.")
    
    return render(request, 'lostqr/signup.html')

# Userhome Wiev
@login_required
def userhome_view(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        # Formu gelen veriyle dolduruyoruz
        form = ProfileForm(request.POST)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # QR Kod İşlemleri
            url = request.build_absolute_uri(f"/p/{profile.id}/")
            import qrcode
            import os
            qr = qrcode.make(url)

            directory = os.path.join(settings.MEDIA_ROOT, "qr_codes")
            os.makedirs(directory, exist_ok=True)
            qr.save(os.path.join(settings.MEDIA_ROOT, "qr_codes", f"{profile.id}.png"))

            return redirect('qrview', profile_id=profile.id)
        
    else:
        form = ProfileForm()

        return render(request, 'lostqr/userhome.html', {
        'form': form,
        'profile': profile
    })


# QR Wiew
@login_required
def qr_view(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)


    url = request.build_absolute_uri(f"/p/{profile.id}/")

    
    qr_path = f"qr_codes/{profile.id}.png"
    full_path = os.path.join(settings.MEDIA_ROOT, qr_path)


    if not os.path.exists(full_path):
        qr = qrcode.make(url)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        qr.save(full_path)

    return render(request, "lostqr/qr_view.html", {
        "profile": profile,
        "url": url,
        "qr_path": f"qr_codes/{profile.id}.png",
    })



# Public Profile View

def public_profile_view(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, "lostqr/public_profile.html", {"profile": profile})
