// static/js/app.js

// جميع الترجمات
const translations = {
  en: {
    // Login
    loginTitle: "Welcome Back",
    loginSubtitle: "Sign in to discover the best nurseries",
    usernameLabel: "Username",
    passwordLabel: "Password",
    rememberLabel: "Remember me",
    forgotPassword: "Forgot Password?",
    signInBtn: "Sign In",
    noAccountText: "Don't have an account?",
    signUpLink: "Sign Up",
    demoText: "Demo Credentials:",

    // Search / results
    searchPlaceholder: "Search for nurseries by name or location...",
    noResultsTitle: "No Results Found",
    noResultsText: "Try different search terms or change the filter",

    forgotMessage:
      "If this were a real system, we would send you a password reset link by email."
  },

  de: {
    // Login
    loginTitle: "Willkommen zurück",
    loginSubtitle:
      "Melden Sie sich an, um die besten Kindergärten zu entdecken",
    usernameLabel: "Benutzername",
    passwordLabel: "Passwort",
    rememberLabel: "Angemeldet bleiben",
    forgotPassword: "Passwort vergessen?",
    signInBtn: "Anmelden",
    noAccountText: "Noch kein Konto?",
    signUpLink: "Registrieren",
    demoText: "Demo-Anmeldedaten:",

    // Search / results
    searchPlaceholder:
      "Suchen Sie nach Kindergärten nach Name oder Standort...",
    noResultsTitle: "Keine Ergebnisse gefunden",
    noResultsText:
      "Versuchen Sie andere Suchbegriffe oder ändern Sie den Filter",

    forgotMessage:
      "In einem echten System würden wir Ihnen einen Link zum Zurücksetzen des Passworts per E-Mail senden."
  },

  ar: {
    // Login
    loginTitle: "مرحباً بعودتك",
    loginSubtitle: "سجل الدخول لاكتشاف أفضل الحضانات",
    usernameLabel: "اسم المستخدم",
    passwordLabel: "كلمة المرور",
    rememberLabel: "تذكرني",
    forgotPassword: "نسيت كلمة المرور؟",
    signInBtn: "تسجيل الدخول",
    noAccountText: "ليس لديك حساب؟",
    signUpLink: "سجل الآن",
    demoText: "بيانات تجريبية:",

    // Search / results
    searchPlaceholder: "ابحث عن حضانة بالاسم أو الموقع...",
    noResultsTitle: "لا توجد نتائج",
    noResultsText:
      "جرّب كلمات بحث مختلفة أو غيّر إعدادات الفلتر",

    forgotMessage:
      "في نظام حقيقي سيتم إرسال رابط لإعادة تعيين كلمة المرور إلى بريدك الإلكتروني."
  }
};

let currentLang = localStorage.getItem("nf_lang") || "en";

// ===== إعداد العملات الجديدة =====
const currencyRates = {
  EUR: 1,
  USD: 1.08,   // تقديري – ممكن تعدليه لو حابة
  AED: 3.95    // تقديري – ممكن تعدليه لو حابة
};

let currentCurrency = localStorage.getItem("nf_currency") || "EUR";

// تفعيل شكل زر اللغة المختار + اتجاه الصفحة
function setActiveLanguageButton(lang) {
  document.querySelectorAll(".language-btn").forEach((btn) => {
    const isActive = btn.dataset.lang === lang;
    btn.classList.toggle("active", isActive);
  });

  // اتجاه النص
  if (lang === "ar") {
    document.documentElement.dir = "rtl";
    document.documentElement.lang = "ar";
  } else {
    document.documentElement.dir = "ltr";
    document.documentElement.lang = lang;
  }
}

// تطبيق الترجمات على العناصر الموجودة
function applyTranslations() {
  const t = translations[currentLang];
  if (!t) return;

  // ===== صفحة تسجيل الدخول =====
  const loginTitle = document.getElementById("loginTitle");
  if (loginTitle) {
    const loginSubtitle = document.getElementById("loginSubtitle");
    const usernameLabel = document.getElementById("usernameLabel");
    const passwordLabel = document.getElementById("passwordLabel");
    const rememberLabel = document.getElementById("rememberLabel");
    const forgotPassword = document.getElementById("forgotPassword");
    const signInBtn = document.getElementById("signInBtn");
    const noAccountText = document.getElementById("noAccountText");
    const signUpLink = document.getElementById("signUpLink");
    const demoText = document.getElementById("demoText");

    loginTitle.textContent = t.loginTitle;
    if (loginSubtitle) loginSubtitle.textContent = t.loginSubtitle;
    if (usernameLabel) usernameLabel.textContent = t.usernameLabel;
    if (passwordLabel) passwordLabel.textContent = t.passwordLabel;
    if (rememberLabel) rememberLabel.textContent = t.rememberLabel;
    if (forgotPassword) forgotPassword.textContent = t.forgotPassword;
    if (signInBtn) signInBtn.textContent = t.signInBtn;
    if (noAccountText) noAccountText.textContent = t.noAccountText;
    if (signUpLink) signUpLink.textContent = t.signUpLink;
    if (demoText) demoText.textContent = t.demoText;
  }

  // ===== صفحة الحضانات / البحث =====
  const searchInput = document.getElementById("searchInput");
  if (searchInput && t.searchPlaceholder) {
    searchInput.placeholder = t.searchPlaceholder;
  }

  const noResultsTitle = document.getElementById("noResultsTitle");
  if (noResultsTitle && t.noResultsTitle) {
    noResultsTitle.textContent = t.noResultsTitle;
  }

  const noResultsText = document.getElementById("noResultsText");
  if (noResultsText && t.noResultsText) {
    noResultsText.textContent = t.noResultsText;
  }
}

// تفعيل Forgot Password كرسالة توضيحية
function setupForgotPassword() {
  const link =
    document.getElementById("forgotPassword") ||
    document.getElementById("forgotPasswordLink");

  if (!link) return;

  link.addEventListener("click", function (e) {
    e.preventDefault();
    const t = translations[currentLang];
    alert(t ? t.forgotMessage : "Password reset flow would go here.");
  });
}

// تفعيل أزرار اللغات
function setupLanguageButtons() {
  document.addEventListener("click", function (e) {
    const btn = e.target.closest(".language-btn");
    if (!btn) return;

    const lang = btn.dataset.lang;
    if (!translations[lang]) return;

    currentLang = lang;
    localStorage.setItem("nf_lang", lang);
    setActiveLanguageButton(lang);
    applyTranslations();
  });
}

/* ====== دوال العملة ====== */

// تنسيق السعر حسب العملة
function formatPrice(eurValue, currencyCode) {
  const rate = currencyRates[currencyCode] || 1;
  const converted = eurValue * rate;

  let symbol = "€";
  if (currencyCode === "USD") symbol = "$";
  else if (currencyCode === "AED") symbol = "AED ";

  return symbol + converted.toFixed(0);
}

// تطبيق العملة على العناصر اللي فيها data-price-eur
function applyCurrency() {
  const priceElements = document.querySelectorAll("[data-price-eur]");
  priceElements.forEach((el) => {
    const eur = parseFloat(el.dataset.priceEur);
    if (isNaN(eur)) return;

    el.textContent = formatPrice(eur, currentCurrency);
  });

  const select = document.getElementById("currencySelect");
  if (select && select.value !== currentCurrency) {
    select.value = currentCurrency;
  }
}

// تفعيل الـ select الخاص بالعملة
function setupCurrencySelector() {
  const select = document.getElementById("currencySelect");
  if (!select) return;

  // اضبط القيمة الابتدائية من localStorage
  if (currencyRates[select.value] === undefined) {
    select.value = currentCurrency;
  }

  select.addEventListener("change", function () {
    currentCurrency = select.value;
    localStorage.setItem("nf_currency", currentCurrency);
    applyCurrency();
  });
}

/* ====== قائمة المستخدم (لو حطيتيها في الـ HTML) ====== */
function setupUserMenu() {
  const btn = document.getElementById("userMenuButton");
  const menu = document.getElementById("userMenu");
  if (!btn || !menu) return;

  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    menu.classList.toggle("hidden");
  });

  // إغلاق القائمة لو المستخدم ضغط برة
  document.addEventListener("click", function () {
    if (!menu.classList.contains("hidden")) {
      menu.classList.add("hidden");
    }
  });
}

// بداية الصفحة
document.addEventListener("DOMContentLoaded", function () {
  setActiveLanguageButton(currentLang);
  applyTranslations();
  setupForgotPassword();
  setupLanguageButtons();

  // العملة + قائمة المستخدم
  applyCurrency();
  setupCurrencySelector();
  setupUserMenu();
});
