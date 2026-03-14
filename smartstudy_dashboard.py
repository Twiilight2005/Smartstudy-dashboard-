import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartStudy AI Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# MULTI-LANGUAGE SYSTEM
# ─────────────────────────────────────────────
LANGUAGES = {
    "🇬🇧 English":  "en",
    "🇮🇳 हिंदी":     "hi",
    "🇮🇳 தமிழ்":    "ta",
    "🇫🇷 Français":  "fr",
    "🇩🇪 Deutsch":   "de",
    "🇯🇵 日本語":     "ja",
    "🇦🇪 العربية":   "ar",
}

TRANSLATIONS = {
    "en": {
        "app_title": "SmartStudy AI",
        "nav_overview": "📊 Overview",
        "nav_weak": "⚠️ Weak Topics",
        "nav_tasks": "✅ Study Tasks",
        "nav_revision": "↺ Revision",
        "nav_progress": "📈 Progress",
        "nav_coach": "🤖 AI Coach",
        "nav_tokens": "🪙 Tokens",
        "next_exam": "Next Exam",
        "days_left": "days left",
        "ai_score": "AI Performance Score",
        "from_last_week": "from last week",
        "study_streak": "Study Streak",
        "tasks_today": "Tasks Today",
        "hours_week": "Hours This Week",
        "exam_in": "Exam In",
        "subject_mastery": "Subject Mastery",
        "weak_alerts": "⚠ Weak Topic Alerts",
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "today_tasks": "Today's Study Tasks",
        "done": "done",
        "revision_today": "↺ Revision Due Today",
        "retention": "retention",
        "spaced_rep": "↺ Spaced Repetition Queue",
        "rep_rules": "Spaced repetition rules",
        "mastery_trend": "Mastery trend (4 weeks)",
        "quiz_acc": "Quiz accuracy by subject",
        "coach_insights": "Coach insights",
        "coach_online": "🟢 SmartStudy AI Coach · Online",
        "quick_q": "Quick questions:",
        "ask_placeholder": "Ask your AI coach...",
        "send": "Send →",
        "clear_chat": "🗑 Clear chat",
        "start": "Start →",
        "mastery_gain": "Mastery gain (4 wks)",
        "consistency": "Study consistency",
        "avg_quiz": "Avg quiz accuracy",
        "avg_speed": "Avg solve speed",
        "token_title": "🪙 Token Rewards",
        "token_balance": "Token Balance",
        "tokens_earned": "Tokens Earned Today",
        "total_earned": "Total Earned",
        "redeemed": "Redeemed",
        "earn_tokens": "How to Earn Tokens",
        "rewards_store": "Rewards Store",
        "leaderboard": "Leaderboard",
        "recent_activity": "Recent Token Activity",
        "redeem": "Redeem",
        "your_badges": "Your Badges",
        "mastery_vs_acc": "Mastery vs quiz accuracy",
        "rec_actions": "Recommended actions",
        "days": "days",
    },
    "hi": {
        "app_title": "स्मार्टस्टडी AI",
        "nav_overview": "📊 अवलोकन",
        "nav_weak": "⚠️ कमज़ोर विषय",
        "nav_tasks": "✅ अध्ययन कार्य",
        "nav_revision": "↺ पुनरावृत्ति",
        "nav_progress": "📈 प्रगति",
        "nav_coach": "🤖 AI कोच",
        "nav_tokens": "🪙 टोकन",
        "next_exam": "अगली परीक्षा",
        "days_left": "दिन बचे",
        "ai_score": "AI प्रदर्शन स्कोर",
        "from_last_week": "पिछले सप्ताह से",
        "study_streak": "अध्ययन स्ट्रीक",
        "tasks_today": "आज के कार्य",
        "hours_week": "इस सप्ताह घंटे",
        "exam_in": "परीक्षा में",
        "subject_mastery": "विषय महारत",
        "weak_alerts": "⚠ कमज़ोर विषय अलर्ट",
        "critical": "गंभीर",
        "high": "उच्च",
        "medium": "मध्यम",
        "today_tasks": "आज के अध्ययन कार्य",
        "done": "पूर्ण",
        "revision_today": "↺ आज की पुनरावृत्ति",
        "retention": "प्रतिधारण",
        "spaced_rep": "↺ स्पेस्ड रिपीटिशन क्यू",
        "rep_rules": "स्पेस्ड रिपीटिशन नियम",
        "mastery_trend": "महारत ट्रेंड (4 सप्ताह)",
        "quiz_acc": "विषय अनुसार क्विज़ सटीकता",
        "coach_insights": "कोच सुझाव",
        "coach_online": "🟢 AI कोच · ऑनलाइन",
        "quick_q": "त्वरित प्रश्न:",
        "ask_placeholder": "अपने AI कोच से पूछें...",
        "send": "भेजें →",
        "clear_chat": "🗑 चैट साफ़ करें",
        "start": "शुरू करें →",
        "mastery_gain": "महारत लाभ (4 सप्ताह)",
        "consistency": "अध्ययन निरंतरता",
        "avg_quiz": "औसत क्विज़ सटीकता",
        "avg_speed": "औसत हल करने की गति",
        "token_title": "🪙 टोकन पुरस्कार",
        "token_balance": "टोकन बैलेंस",
        "tokens_earned": "आज अर्जित टोकन",
        "total_earned": "कुल अर्जित",
        "redeemed": "रिडीम किए",
        "earn_tokens": "टोकन कैसे अर्जित करें",
        "rewards_store": "पुरस्कार स्टोर",
        "leaderboard": "लीडरबोर्ड",
        "recent_activity": "हाल की टोकन गतिविधि",
        "redeem": "रिडीम करें",
        "your_badges": "आपके बैज",
        "mastery_vs_acc": "महारत बनाम क्विज़ सटीकता",
        "rec_actions": "अनुशंसित कार्य",
        "days": "दिन",
    },
    "ta": {
        "app_title": "ஸ்மார்ட்ஸ்டடி AI",
        "nav_overview": "📊 கண்ணோட்டம்",
        "nav_weak": "⚠️ பலவீன தலைப்புகள்",
        "nav_tasks": "✅ படிப்பு பணிகள்",
        "nav_revision": "↺ மறுபார்வை",
        "nav_progress": "📈 முன்னேற்றம்",
        "nav_coach": "🤖 AI பயிற்சியாளர்",
        "nav_tokens": "🪙 டோக்கன்கள்",
        "next_exam": "அடுத்த தேர்வு",
        "days_left": "நாட்கள் உள்ளன",
        "ai_score": "AI செயல்திறன் மதிப்பெண்",
        "from_last_week": "கடந்த வாரத்திலிருந்து",
        "study_streak": "படிப்பு தொடர்ச்சி",
        "tasks_today": "இன்றைய பணிகள்",
        "hours_week": "இந்த வார மணிகள்",
        "exam_in": "தேர்வு",
        "subject_mastery": "பாட தேர்ச்சி",
        "weak_alerts": "⚠ பலவீன தலைப்பு எச்சரிக்கைகள்",
        "critical": "தீவிரம்",
        "high": "அதிகம்",
        "medium": "நடுத்தரம்",
        "today_tasks": "இன்றைய படிப்பு பணிகள்",
        "done": "முடிந்தது",
        "revision_today": "↺ இன்று மறுபார்வை",
        "retention": "தக்கவைப்பு",
        "spaced_rep": "↺ இடைவெளி மறுபார்வை வரிசை",
        "rep_rules": "இடைவெளி மறுபார்வை விதிகள்",
        "mastery_trend": "தேர்ச்சி போக்கு (4 வாரங்கள்)",
        "quiz_acc": "பாட வாரியாக வினாடி வினா துல்லியம்",
        "coach_insights": "பயிற்சியாளர் நுண்ணறிவு",
        "coach_online": "🟢 AI பயிற்சியாளர் · இணைய இணைப்பில்",
        "quick_q": "விரைவு கேள்விகள்:",
        "ask_placeholder": "உங்கள் AI பயிற்சியாளரிடம் கேளுங்கள்...",
        "send": "அனுப்பு →",
        "clear_chat": "🗑 அரட்டையை அழி",
        "start": "தொடங்கு →",
        "mastery_gain": "தேர்ச்சி லாபம் (4 வாரங்கள்)",
        "consistency": "படிப்பு நிலைத்தன்மை",
        "avg_quiz": "சராசரி வினாடி வினா துல்லியம்",
        "avg_speed": "சராசரி தீர்க்கும் வேகம்",
        "token_title": "🪙 டோக்கன் வெகுமதிகள்",
        "token_balance": "டோக்கன் இருப்பு",
        "tokens_earned": "இன்று சம்பாதித்த டோக்கன்கள்",
        "total_earned": "மொத்தம் சம்பாதித்தது",
        "redeemed": "பரிமாறியது",
        "earn_tokens": "டோக்கன்கள் எவ்வாறு சம்பாதிப்பது",
        "rewards_store": "வெகுமதி கடை",
        "leaderboard": "தரவரிசை பட்டியல்",
        "recent_activity": "சமீபத்திய டோக்கன் செயல்பாடு",
        "redeem": "பரிமாறு",
        "your_badges": "உங்கள் பதக்கங்கள்",
        "mastery_vs_acc": "தேர்ச்சி vs வினாடி வினா துல்லியம்",
        "rec_actions": "பரிந்துரைக்கப்பட்ட செயல்கள்",
        "days": "நாட்கள்",
    },
    "fr": {
        "app_title": "SmartStudy IA",
        "nav_overview": "📊 Aperçu",
        "nav_weak": "⚠️ Sujets faibles",
        "nav_tasks": "✅ Tâches d'étude",
        "nav_revision": "↺ Révision",
        "nav_progress": "📈 Progrès",
        "nav_coach": "🤖 Coach IA",
        "nav_tokens": "🪙 Jetons",
        "next_exam": "Prochain examen",
        "days_left": "jours restants",
        "ai_score": "Score de performance IA",
        "from_last_week": "par rapport à la semaine dernière",
        "study_streak": "Série d'études",
        "tasks_today": "Tâches aujourd'hui",
        "hours_week": "Heures cette semaine",
        "exam_in": "Examen dans",
        "subject_mastery": "Maîtrise des matières",
        "weak_alerts": "⚠ Alertes sujets faibles",
        "critical": "Critique",
        "high": "Élevé",
        "medium": "Moyen",
        "today_tasks": "Tâches d'étude du jour",
        "done": "terminé",
        "revision_today": "↺ Révision prévue aujourd'hui",
        "retention": "rétention",
        "spaced_rep": "↺ File de répétition espacée",
        "rep_rules": "Règles de répétition espacée",
        "mastery_trend": "Tendance de maîtrise (4 semaines)",
        "quiz_acc": "Précision des quiz par matière",
        "coach_insights": "Conseils du coach",
        "coach_online": "🟢 Coach IA SmartStudy · En ligne",
        "quick_q": "Questions rapides :",
        "ask_placeholder": "Posez une question à votre coach IA...",
        "send": "Envoyer →",
        "clear_chat": "🗑 Effacer le chat",
        "start": "Commencer →",
        "mastery_gain": "Gain de maîtrise (4 sem.)",
        "consistency": "Régularité des études",
        "avg_quiz": "Précision moy. des quiz",
        "avg_speed": "Vitesse moy. de résolution",
        "token_title": "🪙 Récompenses en jetons",
        "token_balance": "Solde de jetons",
        "tokens_earned": "Jetons gagnés aujourd'hui",
        "total_earned": "Total gagné",
        "redeemed": "Échangés",
        "earn_tokens": "Comment gagner des jetons",
        "rewards_store": "Boutique de récompenses",
        "leaderboard": "Classement",
        "recent_activity": "Activité récente de jetons",
        "redeem": "Échanger",
        "your_badges": "Vos badges",
        "mastery_vs_acc": "Maîtrise vs précision",
        "rec_actions": "Actions recommandées",
        "days": "jours",
    },
    "de": {
        "app_title": "SmartStudy KI",
        "nav_overview": "📊 Übersicht",
        "nav_weak": "⚠️ Schwache Themen",
        "nav_tasks": "✅ Lernaufgaben",
        "nav_revision": "↺ Wiederholung",
        "nav_progress": "📈 Fortschritt",
        "nav_coach": "🤖 KI-Coach",
        "nav_tokens": "🪙 Token",
        "next_exam": "Nächste Prüfung",
        "days_left": "Tage verbleibend",
        "ai_score": "KI-Leistungspunktzahl",
        "from_last_week": "gegenüber letzter Woche",
        "study_streak": "Lernserie",
        "tasks_today": "Aufgaben heute",
        "hours_week": "Stunden diese Woche",
        "exam_in": "Prüfung in",
        "subject_mastery": "Fachkenntnisse",
        "weak_alerts": "⚠ Schwache Themen Alerts",
        "critical": "Kritisch",
        "high": "Hoch",
        "medium": "Mittel",
        "today_tasks": "Heutige Lernaufgaben",
        "done": "erledigt",
        "revision_today": "↺ Wiederholung heute fällig",
        "retention": "Behaltensrate",
        "spaced_rep": "↺ Spaced-Repetition-Warteschlange",
        "rep_rules": "Spaced-Repetition-Regeln",
        "mastery_trend": "Lerntrend (4 Wochen)",
        "quiz_acc": "Quiz-Genauigkeit nach Fach",
        "coach_insights": "Coach-Einblicke",
        "coach_online": "🟢 SmartStudy KI-Coach · Online",
        "quick_q": "Schnellfragen:",
        "ask_placeholder": "Fragen Sie Ihren KI-Coach...",
        "send": "Senden →",
        "clear_chat": "🗑 Chat löschen",
        "start": "Starten →",
        "mastery_gain": "Lerngewinn (4 Wo.)",
        "consistency": "Lernkontinuität",
        "avg_quiz": "Ø Quiz-Genauigkeit",
        "avg_speed": "Ø Lösungsgeschwindigkeit",
        "token_title": "🪙 Token-Belohnungen",
        "token_balance": "Token-Guthaben",
        "tokens_earned": "Heute verdiente Token",
        "total_earned": "Gesamt verdient",
        "redeemed": "Eingelöst",
        "earn_tokens": "Wie man Token verdient",
        "rewards_store": "Belohnungsshop",
        "leaderboard": "Bestenliste",
        "recent_activity": "Letzte Token-Aktivitäten",
        "redeem": "Einlösen",
        "your_badges": "Ihre Abzeichen",
        "mastery_vs_acc": "Kenntnisse vs. Genauigkeit",
        "rec_actions": "Empfohlene Maßnahmen",
        "days": "Tage",
    },
    "ja": {
        "app_title": "スマートスタディ AI",
        "nav_overview": "📊 概要",
        "nav_weak": "⚠️ 弱いトピック",
        "nav_tasks": "✅ 学習タスク",
        "nav_revision": "↺ 復習",
        "nav_progress": "📈 進捗",
        "nav_coach": "🤖 AIコーチ",
        "nav_tokens": "🪙 トークン",
        "next_exam": "次の試験",
        "days_left": "日残り",
        "ai_score": "AIパフォーマンススコア",
        "from_last_week": "先週比",
        "study_streak": "学習連続記録",
        "tasks_today": "今日のタスク",
        "hours_week": "今週の学習時間",
        "exam_in": "試験まで",
        "subject_mastery": "科目習熟度",
        "weak_alerts": "⚠ 弱点アラート",
        "critical": "緊急",
        "high": "高",
        "medium": "中",
        "today_tasks": "今日の学習タスク",
        "done": "完了",
        "revision_today": "↺ 今日の復習",
        "retention": "定着率",
        "spaced_rep": "↺ 間隔反復キュー",
        "rep_rules": "間隔反復ルール",
        "mastery_trend": "習熟度トレンド（4週間）",
        "quiz_acc": "科目別クイズ正解率",
        "coach_insights": "コーチのアドバイス",
        "coach_online": "🟢 AIコーチ · オンライン",
        "quick_q": "クイック質問：",
        "ask_placeholder": "AIコーチに質問する...",
        "send": "送信 →",
        "clear_chat": "🗑 チャットをクリア",
        "start": "開始 →",
        "mastery_gain": "習熟度向上（4週間）",
        "consistency": "学習継続率",
        "avg_quiz": "平均クイズ正解率",
        "avg_speed": "平均解答速度",
        "token_title": "🪙 トークン報酬",
        "token_balance": "トークン残高",
        "tokens_earned": "今日獲得したトークン",
        "total_earned": "合計獲得",
        "redeemed": "交換済み",
        "earn_tokens": "トークンの獲得方法",
        "rewards_store": "報酬ストア",
        "leaderboard": "ランキング",
        "recent_activity": "最近のトークン活動",
        "redeem": "交換する",
        "your_badges": "バッジ",
        "mastery_vs_acc": "習熟度 vs クイズ正解率",
        "rec_actions": "推奨アクション",
        "days": "日",
    },
    "ar": {
        "app_title": "سمارت ستادي",
        "nav_overview": "📊 نظرة عامة",
        "nav_weak": "⚠️ المواضيع الضعيفة",
        "nav_tasks": "✅ مهام الدراسة",
        "nav_revision": "↺ المراجعة",
        "nav_progress": "📈 التقدم",
        "nav_coach": "🤖 المدرب الذكي",
        "nav_tokens": "🪙 الرموز",
        "next_exam": "الامتحان القادم",
        "days_left": "أيام متبقية",
        "ai_score": "درجة الأداء الذكي",
        "from_last_week": "مقارنة بالأسبوع الماضي",
        "study_streak": "سلسلة الدراسة",
        "tasks_today": "مهام اليوم",
        "hours_week": "ساعات هذا الأسبوع",
        "exam_in": "الامتحان في",
        "subject_mastery": "إتقان المواد",
        "weak_alerts": "⚠ تنبيهات المواضيع الضعيفة",
        "critical": "حرج",
        "high": "عالي",
        "medium": "متوسط",
        "today_tasks": "مهام الدراسة اليوم",
        "done": "مكتمل",
        "revision_today": "↺ المراجعة المستحقة اليوم",
        "retention": "الاحتفاظ",
        "spaced_rep": "↺ قائمة التكرار المتباعد",
        "rep_rules": "قواعد التكرار المتباعد",
        "mastery_trend": "اتجاه الإتقان (4 أسابيع)",
        "quiz_acc": "دقة الاختبارات حسب المادة",
        "coach_insights": "رؤى المدرب",
        "coach_online": "🟢 المدرب الذكي · متصل",
        "quick_q": "أسئلة سريعة:",
        "ask_placeholder": "اسأل مدربك الذكي...",
        "send": "إرسال →",
        "clear_chat": "🗑 مسح المحادثة",
        "start": "ابدأ →",
        "mastery_gain": "مكسب الإتقان (4 أسابيع)",
        "consistency": "انتظام الدراسة",
        "avg_quiz": "متوسط دقة الاختبار",
        "avg_speed": "متوسط سرعة الحل",
        "token_title": "🪙 مكافآت الرموز",
        "token_balance": "رصيد الرموز",
        "tokens_earned": "الرموز المكتسبة اليوم",
        "total_earned": "إجمالي المكتسب",
        "redeemed": "تم الاستبدال",
        "earn_tokens": "كيفية كسب الرموز",
        "rewards_store": "متجر المكافآت",
        "leaderboard": "لوحة المتصدرين",
        "recent_activity": "نشاط الرموز الأخير",
        "redeem": "استبدال",
        "your_badges": "شاراتك",
        "mastery_vs_acc": "الإتقان مقابل الدقة",
        "rec_actions": "الإجراءات الموصى بها",
        "days": "أيام",
    },
}

def T(key: str) -> str:
    """Get translated string for current language."""
    lang_code = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang_code, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))

# ─────────────────────────────────────────────
# TOKEN INCENTIVE SYSTEM DATA
# ─────────────────────────────────────────────
TOKEN_RULES = [
    {"action": "Complete a study task",         "tokens": 10,  "icon": "✅"},
    {"action": "Finish all daily tasks (5/5)",   "tokens": 50,  "icon": "🎯"},
    {"action": "Pass a quiz (score ≥ 70%)",       "tokens": 25,  "icon": "📝"},
    {"action": "Ace a quiz (score ≥ 90%)",        "tokens": 60,  "icon": "🏆"},
    {"action": "Complete a revision session",    "tokens": 15,  "icon": "↺"},
    {"action": "Maintain a 7-day streak",        "tokens": 100, "icon": "🔥"},
    {"action": "Improve a weak topic by +10pts", "tokens": 75,  "icon": "📈"},
    {"action": "Study for 2h in one day",        "tokens": 30,  "icon": "⏱"},
    {"action": "Watch a recommended video",      "tokens": 5,   "icon": "📹"},
    {"action": "Unlock a new subject milestone", "tokens": 150, "icon": "🎖"},
]

REWARDS_STORE = [
    {"name": "Skip 1 revision session",  "cost": 100, "icon": "⏭",  "category": "Flexibility"},
    {"name": "Unlock dark theme pro",    "cost": 200, "icon": "🌙",  "category": "Cosmetic"},
    {"name": "Extra AI coach query",     "cost": 50,  "icon": "🤖",  "category": "Feature"},
    {"name": "Get a study certificate",  "cost": 500, "icon": "🏅",  "category": "Achievement"},
    {"name": "Unlock bonus quiz pack",   "cost": 150, "icon": "📦",  "category": "Content"},
    {"name": "Custom avatar frame",      "cost": 300, "icon": "🖼",  "category": "Cosmetic"},
    {"name": "1 free mock exam",         "cost": 400, "icon": "📋",  "category": "Content"},
    {"name": "Streak freeze (1 day)",    "cost": 80,  "icon": "❄️",  "category": "Flexibility"},
]

LEADERBOARD = [
    {"rank": 1,  "name": "Priya S.",      "tokens": 4820, "badge": "🥇", "streak": 28},
    {"rank": 2,  "name": "Rohan M.",      "tokens": 4310, "badge": "🥈", "streak": 21},
    {"rank": 3,  "name": "Ananya K.",     "tokens": 3950, "badge": "🥉", "streak": 19},
    {"rank": 4,  "name": "Arjun R. (You)","tokens": 3640, "badge": "⭐", "streak": 14},
    {"rank": 5,  "name": "Kavya T.",      "tokens": 3210, "badge": "",   "streak": 12},
    {"rank": 6,  "name": "Dev P.",        "tokens": 2980, "badge": "",   "streak": 10},
    {"rank": 7,  "name": "Meera L.",      "tokens": 2750, "badge": "",   "streak": 8},
]

TOKEN_ACTIVITY = [
    {"action": "Completed all 5 tasks",         "tokens": "+50",  "time": "Today 19:30",  "color": "#4ade80"},
    {"action": "Aced Python quiz (94%)",         "tokens": "+60",  "time": "Today 16:45",  "color": "#4ade80"},
    {"action": "Revision session — Integration", "tokens": "+15",  "time": "Today 14:10",  "color": "#4ade80"},
    {"action": "14-day streak bonus",            "tokens": "+100", "time": "Today 09:00",  "color": "#fbbf24"},
    {"action": "Improved Thermodynamics +11pts", "tokens": "+75",  "time": "Yesterday",    "color": "#4ade80"},
    {"action": "Redeemed: Extra AI query",       "tokens": "−50",  "time": "2 days ago",   "color": "#f87171"},
]

BADGES = [
    {"name": "Streak Master",   "icon": "🔥", "desc": "14-day streak",     "earned": True},
    {"name": "Quiz Ace",        "icon": "🏆", "desc": "Score 90%+ in quiz","earned": True},
    {"name": "Night Owl",       "icon": "🦉", "desc": "Study after 10pm",  "earned": True},
    {"name": "Comeback Kid",    "icon": "💪", "desc": "Improve weak topic", "earned": True},
    {"name": "Speed Solver",    "icon": "⚡", "desc": "Under 1min/question","earned": False},
    {"name": "Perfect Week",    "icon": "🌟", "desc": "7/7 days complete",  "earned": False},
    {"name": "Century Club",    "icon": "💯", "desc": "Score 100% in quiz", "earned": False},
    {"name": "Token Millionaire","icon":"💎",  "desc": "Earn 5000 tokens",   "earned": False},
]

# ─────────────────────────────────────────────
# GLOBAL CSS  (dark theme matching the prototype)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0d0f14;
    color: #e2e8f0;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 1.5rem 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #141720 !important;
    border-right: 1px solid #2a2f3e;
}
[data-testid="stSidebar"] * { color: #8892a4 !important; }
[data-testid="stSidebar"] .sidebar-title {
    color: #e2e8f0 !important;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #1a1e2a;
    border: 1px solid #2a2f3e;
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #8892a4 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 26px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* ── Cards ── */
.dash-card {
    background: #141720;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #555f72;
    text-transform: uppercase;
    margin-bottom: 14px;
}

/* ── Priority badges ── */
.badge-critical {
    background: #3d0f0f; color: #f87171;
    border: 1px solid #f8717144;
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    display: inline-block;
}
.badge-high {
    background: #2d1a06; color: #fb923c;
    border: 1px solid #fb923c44;
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    display: inline-block;
}
.badge-medium {
    background: #2d2206; color: #fbbf24;
    border: 1px solid #fbbf2444;
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    display: inline-block;
}

/* ── Task rows ── */
.task-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #2a2f3e;
    font-size: 14px;
}
.task-done { text-decoration: line-through; color: #555f72; }
.tag { font-size: 10px; padding: 3px 9px; border-radius: 10px; font-weight: 500; }
.tag-study    { background:#1e2a1e; color:#4ade80; border:1px solid #4ade8044; }
.tag-practice { background:#1a1f2e; color:#38bdf8; border:1px solid #38bdf844; }
.tag-revise   { background:#261a2e; color:#a78bfa; border:1px solid #a78bfa44; }
.tag-project  { background:#1e2226; color:#00c9a7; border:1px solid #00c9a744; }
.tag-quiz     { background:#2a1e2a; color:#f472b6; border:1px solid #f472b644; }

/* ── Revision items ── */
.rev-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 12px;
    background: #1a1e2a; border-radius: 10px;
    margin-bottom: 8px;
}

/* ── Streak / date badges in header ── */
.streak-badge {
    background: #2a1f0a; color: #fb923c;
    border: 1px solid #fb923c44;
    font-size: 13px; font-weight: 600;
    padding: 6px 14px; border-radius: 20px;
    display: inline-block;
}
.date-badge {
    background: #1a1e2a; color: #8892a4;
    border: 1px solid #2a2f3e;
    font-size: 13px;
    padding: 6px 14px; border-radius: 20px;
    display: inline-block;
}

/* ── Chat ── */
.chat-wrap {
    background: #141720;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    overflow: hidden;
}
.chat-header {
    padding: 10px 16px;
    background: #1a1e2a;
    border-bottom: 1px solid #2a2f3e;
    font-size: 13px; font-weight: 600; color: #e2e8f0;
}
.msg-ai {
    background: #1a1e2a; color: #e2e8f0;
    border: 1px solid #2a2f3e;
    border-radius: 10px; padding: 10px 13px;
    font-size: 13px; line-height: 1.6;
    margin-bottom: 8px; max-width: 82%;
}
.msg-user {
    background: linear-gradient(135deg,#1a3a30,#1a2040);
    color: #00c9a7;
    border: 1px solid #00c9a733;
    border-radius: 10px; padding: 10px 13px;
    font-size: 13px; line-height: 1.6;
    margin-bottom: 8px; max-width: 82%;
    margin-left: auto;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: #1a1e2a !important;
    border: 1px solid #2a2f3e !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: #00c9a7 !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}
.stButton > button:hover {
    background: #00b090 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #141720;
    border-bottom: 1px solid #2a2f3e;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8892a4 !important;
    border-radius: 8px 8px 0 0 !important;
    font-size: 13px !important;
}
.stTabs [aria-selected="true"] {
    color: #00c9a7 !important;
    border-bottom: 2px solid #00c9a7 !important;
    background: #1a1e2a !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #0d0f14 !important;
    padding: 16px 0 !important;
}

/* ── Selectbox / radio ── */
.stSelectbox > div > div,
.stRadio > div { background: #1a1e2a !important; border-color: #2a2f3e !important; }

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00c9a7, #a78bfa) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────────────
STUDENT = {
    "name": "Arjun Rajan",
    "grade": "Grade 11 · Science",
    "streak": 14,
    "ai_score": 74.2,
    "score_delta": 3.8,
    "tasks_today": 5,
    "tasks_total": 5,
    "hours_week": 18.5,
    "exam": {"name": "Physics Final", "days_left": 12},
}

SUBJECTS = [
    {"name": "Mathematics", "pct": 54, "color": "#fb923c"},
    {"name": "Physics",      "pct": 71, "color": "#a78bfa"},
    {"name": "Programming",  "pct": 88, "color": "#00c9a7"},
    {"name": "Chemistry",    "pct": 43, "color": "#f472b6"},
    {"name": "English",      "pct": 76, "color": "#38bdf8"},
]

WEAK_TOPICS = [
    {"name": "Organic Reactions",    "subject": "Chemistry",    "dot": "#f472b6", "priority": "Critical", "score": 28, "reason": "28% mastery · 3 repeated errors · low quiz accuracy 24%"},
    {"name": "Differential Calculus","subject": "Mathematics",  "dot": "#fb923c", "priority": "High",     "score": 41, "reason": "41% mastery · slow solving speed · 5-day revision gap"},
    {"name": "Matrix Algebra",       "subject": "Mathematics",  "dot": "#fb923c", "priority": "High",     "score": 48, "reason": "48% mastery · consistent first-attempt errors"},
    {"name": "Electromagnetism",     "subject": "Physics",      "dot": "#a78bfa", "priority": "Medium",   "score": 62, "reason": "62% mastery · VSEPR / field lines confusion"},
    {"name": "Newton's Laws",        "subject": "Physics",      "dot": "#a78bfa", "priority": "Medium",   "score": 61, "reason": "61% retention · 14 days since last revision"},
]

TASKS = [
    {"time": "09:00", "name": "Organic Reactions",    "meta": "Chemistry · 45 min",    "tag": "Study",    "tag_class": "tag-study",    "done": True},
    {"time": "10:00", "name": "Differential Calculus","meta": "Mathematics · 60 min",  "tag": "Practice", "tag_class": "tag-practice", "done": True},
    {"time": "14:00", "name": "Electromagnetism",     "meta": "Physics · 45 min",      "tag": "Revise",   "tag_class": "tag-revise",   "done": True},
    {"time": "16:00", "name": "Data Structures",      "meta": "Programming · 90 min",  "tag": "Project",  "tag_class": "tag-project",  "done": True},
    {"time": "19:00", "name": "Matrix Algebra",       "meta": "Mathematics · 30 min",  "tag": "Quiz",     "tag_class": "tag-quiz",     "done": True},
]

REVISIONS = [
    {"name": "Quadratic Equations", "meta": "Mathematics · 7d ago",  "icon": "📐", "retention": 72,  "ret_color": "#fbbf24", "interval": "1-day"},
    {"name": "Newton's Laws",       "meta": "Physics · 14d ago",     "icon": "⚡", "retention": 61,  "ret_color": "#fb923c", "interval": "1-day"},
    {"name": "Python Functions",    "meta": "Programming · 3d ago",  "icon": "💻", "retention": 88,  "ret_color": "#4ade80", "interval": "7-day"},
    {"name": "Integration",         "meta": "Mathematics · 2d ago",  "icon": "∫",  "retention": 71,  "ret_color": "#a78bfa", "interval": "3-day"},
]

MASTERY_TREND = {
    "weeks": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "overall":     [66, 69, 71, 74],
    "chemistry":   [30, 34, 38, 43],
    "programming": [80, 84, 86, 88],
    "physics":     [64, 66, 69, 71],
}

QUIZ_ACCURACY = {
    "subjects": ["Programming", "English", "Physics", "Mathematics", "Chemistry"],
    "accuracy": [91, 78, 68, 52, 24],
    "colors":   ["#00c9a7", "#38bdf8", "#a78bfa", "#fb923c", "#f87171"],
}

AI_RESPONSES = {
    "What should I study today?":
        "📌 Based on your weak topics and today's schedule:\n\n"
        "1. **Organic Reactions** (45 min) — Chemistry at 28%, critical priority.\n"
        "2. **Differential Calculus** revision (30 min) — score 41%, 1-day interval due.\n"
        "3. **Matrix Algebra** quiz (20 min) — 48%, needs frequent reinforcement.\n\n"
        "You've already completed 5/5 tasks today — amazing consistency! 🎯",
    "Why is Organic Reactions weak?":
        "🔍 **Organic Reactions breakdown:**\n\n"
        "• Mastery score: **28/100** — Critical\n"
        "• Quiz accuracy: only **24%**\n"
        "• Repeated errors in: mechanism reactions, reagent identification\n"
        "• Root cause: concepts unclear before practice\n\n"
        "**Recommendation:** Watch reaction mechanism videos first, then attempt MCQs. Revise daily until score crosses 50.",
    "Show my progress this week":
        "📊 **This week's progress report:**\n\n"
        "• AI Score: **74.2** (↑3.8 from last week) ⭐\n"
        "• Programming: **88%** — your best subject!\n"
        "• Study streak: **14 days** — phenomenal!\n"
        "• Tasks completed: **5/5** today\n"
        "• Chemistry still critical at **28%** — needs daily work.\n\n"
        "Overall trend is positive. Keep Chemistry as your #1 focus this week.",
    "Plan my exam week":
        "📅 **Exam prep plan (7 days):**\n\n"
        "**Day 1–2:** Organic Reactions intensive (1h/day) + Calculus revision\n"
        "**Day 3–4:** Matrix Algebra drills + Physics mock tests\n"
        "**Day 5:** Full Chemistry mock paper\n"
        "**Day 6:** Error analysis — redo all wrong answers\n"
        "**Day 7:** Light revision only + good rest\n\n"
        "This prioritises your 3 critical weak topics while protecting strong subjects.",
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#8892a4",
    font_family="Space Grotesk",
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8892a4", size=11),
    ),
)

GRID_STYLE = dict(
    gridcolor="#1f2435",
    linecolor="#2a2f3e",
    tickfont=dict(color="#8892a4", size=10),
    zerolinecolor="#2a2f3e",
)


def gauge_ring(value: int, color: str, size: int = 110) -> go.Figure:
    fig = go.Figure(go.Pie(
        values=[value, 100 - value],
        hole=0.72,
        marker_colors=[color, "#1f2435"],
        textinfo="none",
        hoverinfo="skip",
        sort=False,
    ))
    fig.update_layout(
        width=size, height=size,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        annotations=[dict(
            text=f"<b>{value}%</b>",
            x=0.5, y=0.5,
            font=dict(size=16, color="#e2e8f0", family="Space Grotesk"),
            showarrow=False,
        )],
    )
    return fig


def priority_badge_html(priority: str) -> str:
    cls = {"Critical": "badge-critical", "High": "badge-high", "Medium": "badge-medium"}.get(priority, "badge-medium")
    return f'<span class="{cls}">{priority}</span>'


def score_color(score: int) -> str:
    if score < 40:  return "#f87171"
    if score < 60:  return "#fb923c"
    if score < 75:  return "#fbbf24"
    return "#4ade80"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div class="sidebar-title">{T("app_title")}</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Student card with token mini-display
    st.markdown(f"""
    <div style="background:#1a1e2a;border:1px solid #2a2f3e;border-radius:12px;padding:14px;margin-bottom:14px">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#a78bfa,#00c9a7);
                 display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;color:#0d0f14">A</div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#e2e8f0">{STUDENT['name']}</div>
                <div style="font-size:11px;color:#8892a4">{STUDENT['grade']}</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between">
            <span class="streak-badge">🔥 {STUDENT['streak']}-{T('days')}</span>
            <span style="background:#2a1f06;color:#fbbf24;border:1px solid #fbbf2444;
                         font-size:11px;font-weight:600;padding:4px 10px;border-radius:20px">
                🪙 {st.session_state.tokens:,}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation (translated labels)
    nav_options = [
        T("nav_overview"), T("nav_weak"), T("nav_tasks"),
        T("nav_revision"), T("nav_progress"), T("nav_coach"), T("nav_tokens"),
    ]
    page = st.radio(
        "Navigation",
        nav_options,
        label_visibility="collapsed",
    )

    # Exam countdown
    st.markdown(f"""
    <div style="background:#1a1e2a;border:1px solid #2a2f3e;border-radius:12px;padding:14px;margin-top:16px">
        <div style="font-size:10px;font-weight:600;letter-spacing:1.2px;color:#555f72;text-transform:uppercase;margin-bottom:4px">{T('next_exam')}</div>
        <div style="font-size:13px;font-weight:600;color:#e2e8f0">{STUDENT['exam']['name']}</div>
        <div style="font-size:26px;font-weight:700;color:#f87171;line-height:1.2">{STUDENT['exam']['days_left']}
            <span style="font-size:12px;color:#8892a4">{T('days_left')}</span></div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LANGUAGE INIT
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "tokens" not in st.session_state:
    st.session_state.tokens = 3640
if "tokens_today" not in st.session_state:
    st.session_state.tokens_today = 300

# ─────────────────────────────────────────────
# TOPBAR  (with language selector top-right)
# ─────────────────────────────────────────────
today_str = datetime.now().strftime("%a, %b %d")
tb_left, tb_mid, tb_right = st.columns([3, 4, 3])

with tb_left:
    st.markdown(f"""
    <div style="background:#141720;border:1px solid #2a2f3e;border-radius:12px;
                padding:12px 20px;height:54px;display:flex;align-items:center;gap:12px">
        <span style="font-size:18px;font-weight:700;color:#e2e8f0">{T('app_title')}</span>
        <span class="streak-badge">🔥 {STUDENT['streak']} {T('days')}</span>
        <span class="date-badge">{today_str}</span>
    </div>
    """, unsafe_allow_html=True)

with tb_mid:
    st.markdown(f"""
    <div style="background:#141720;border:1px solid #2a2f3e;border-radius:12px;
                padding:8px 16px;height:54px;display:flex;align-items:center;gap:16px">
        <div style="display:flex;align-items:center;gap:8px">
            <span style="font-size:18px">🪙</span>
            <div>
                <div style="font-size:11px;color:#8892a4;line-height:1">{T('token_balance')}</div>
                <div style="font-size:17px;font-weight:700;color:#fbbf24">{st.session_state.tokens:,}</div>
            </div>
        </div>
        <div style="width:1px;height:28px;background:#2a2f3e"></div>
        <div style="font-size:12px;color:#4ade80">+{st.session_state.tokens_today} {T('tokens_earned')}</div>
    </div>
    """, unsafe_allow_html=True)

with tb_right:
    lang_col1, lang_col2 = st.columns([0.4, 0.6])
    with lang_col1:
        st.markdown('<div style="padding-top:14px;font-size:12px;color:#8892a4;text-align:right">🌐 Language</div>', unsafe_allow_html=True)
    with lang_col2:
        lang_choice = st.selectbox(
            "lang_select",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.values()).index(st.session_state.lang),
            label_visibility="collapsed",
            key="lang_selector",
        )
        new_lang = LANGUAGES[lang_choice]
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════
if page == T("nav_overview"):

    # ── AI Performance Score ──
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"""
        <div class="section-label">{T('ai_score')}</div>
        <div style="font-size:52px;font-weight:700;color:#e2e8f0;line-height:1">{STUDENT['ai_score']}</div>
        <div style="color:#4ade80;font-size:13px;font-weight:500;margin-top:6px">▲ +{STUDENT['score_delta']} {T('from_last_week')}</div>
        """, unsafe_allow_html=True)
    with c2:
        fig = gauge_ring(74, "#00c9a7", size=120)
        fig.update_layout(
            annotations=[dict(
                text="<b>74%</b><br><span style='font-size:10px'>Overall</span>",
                x=0.5, y=0.5,
                font=dict(size=15, color="#e2e8f0"),
                showarrow=False,
            )]
        )
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Stat boxes ──
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"🔥 {T('study_streak')}",    f"{STUDENT['streak']} {T('days')}")
    m2.metric(f"✓  {T('tasks_today')}",     f"{STUDENT['tasks_today']}/{STUDENT['tasks_total']}")
    m3.metric(f"⏱  {T('hours_week')}", f"{STUDENT['hours_week']} h")
    m4.metric(f"📅 {T('exam_in')}",         f"{STUDENT['exam']['days_left']} {T('days')}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Subject mastery rings ──
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T("subject_mastery")}</div>', unsafe_allow_html=True)
    cols = st.columns(len(SUBJECTS))
    for col, s in zip(cols, SUBJECTS):
        with col:
            fig = gauge_ring(s["pct"], s["color"], size=90)
            st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
            st.markdown(f'<div style="text-align:center;font-size:11px;color:#8892a4;margin-top:-8px">{s["name"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Weak Topic Alerts ──
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([3, 1])
    hcol1.markdown(f'<div class="section-label" style="margin-bottom:0">{T("weak_alerts")}</div>', unsafe_allow_html=True)
    hcol2.markdown(f'<div style="text-align:right"><span style="background:#3d0f0f;color:#f87171;border:1px solid #f8717144;font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px">3 {T("critical")}</span></div>', unsafe_allow_html=True)

    for w in WEAK_TOPICS[:3]:
        sc = score_color(w["score"])
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid #2a2f3e">
            {priority_badge_html(w['priority'])}
            <div style="flex:1">
                <div style="font-size:14px;font-weight:600;color:#e2e8f0">{w['name']}</div>
                <div style="font-size:12px;color:{w['dot']};margin-top:2px">⬤ {w['subject']}</div>
            </div>
            <div style="font-size:16px;font-weight:700;color:{sc}">{w['score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: WEAK TOPICS
# ═══════════════════════════════════════════════
elif page == T("nav_weak"):

    # Alert list
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([3, 1])
    hcol1.markdown(f'<div class="section-label" style="margin-bottom:0">{T("weak_alerts")}</div>', unsafe_allow_html=True)
    hcol2.markdown(f'<div style="text-align:right"><span style="background:#3d0f0f;color:#f87171;border:1px solid #f8717144;font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px">3 {T("critical")}</span></div>', unsafe_allow_html=True)

    for w in WEAK_TOPICS:
        sc = score_color(w["score"])
        bar_pct = w["score"]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid #2a2f3e">
            {priority_badge_html(w['priority'])}
            <div style="flex:1">
                <div style="font-size:14px;font-weight:600;color:#e2e8f0">{w['name']}</div>
                <div style="font-size:11px;color:#8892a4;margin-top:2px">{w['reason']}</div>
                <div style="height:4px;background:#1f2435;border-radius:2px;margin-top:6px;overflow:hidden">
                    <div style="width:{bar_pct}%;height:4px;background:{sc};border-radius:2px"></div>
                </div>
            </div>
            <div style="font-size:18px;font-weight:700;color:{sc};min-width:42px;text-align:right">{w['score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("mastery_vs_acc")}</div>', unsafe_allow_html=True)
        names = [w["name"] for w in WEAK_TOPICS]
        mastery  = [w["score"] for w in WEAK_TOPICS]
        accuracy = [w["score"] - 4 for w in WEAK_TOPICS]  # simulated
        fig = go.Figure()
        fig.add_bar(name="Mastery",       x=names, y=mastery,  marker_color="#a78bfa")
        fig.add_bar(name="Quiz Accuracy", x=names, y=accuracy, marker_color="#00c9a7")
        fig.update_layout(**PLOT_LAYOUT, barmode="group", height=260,
                          xaxis=dict(**GRID_STYLE, tickangle=-25),
                          yaxis=dict(**GRID_STYLE, range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("rec_actions")}</div>', unsafe_allow_html=True)
        actions = [
            ("#f87171", "Study Organic Reactions 45 min today. Focus on mechanism reactions — you've missed this 3×."),
            ("#fb923c", "Practice Calculus MCQs daily to build speed. Target: under 2 min/Q by next week."),
            ("#fbbf24", "Revise Matrix Algebra using flashcards — eigenvalues and determinants first."),
        ]
        for color, text in actions:
            st.markdown(f"""
            <div style="padding:10px;background:#1a1e2a;border-radius:10px;border-left:3px solid {color};
                        font-size:12px;color:#e2e8f0;line-height:1.6;margin-bottom:8px">{text}</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: STUDY TASKS
# ═══════════════════════════════════════════════
elif page == T("nav_tasks"):

    if "tasks" not in st.session_state:
        st.session_state.tasks = [t.copy() for t in TASKS]

    done_count = sum(1 for t in st.session_state.tasks if t["done"])
    total = len(st.session_state.tasks)
    progress = done_count / total

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([3, 1])
    hcol1.markdown(f'<div class="section-label" style="margin-bottom:0">{T("today_tasks")}</div>', unsafe_allow_html=True)
    hcol2.markdown(f'<div style="text-align:right;font-size:14px;font-weight:600;color:#00c9a7">{done_count}/{total} {T("done")}</div>', unsafe_allow_html=True)

    st.progress(progress)

    for i, task in enumerate(st.session_state.tasks):
        c1, c2, c3, c4, c5 = st.columns([0.4, 0.7, 2.5, 1.2, 0.8])
        with c1:
            checked = st.checkbox("", value=task["done"], key=f"task_{i}", label_visibility="collapsed")
            st.session_state.tasks[i]["done"] = checked
        with c2:
            st.markdown(f'<div style="font-size:12px;color:#555f72;padding-top:6px">{task["time"]}</div>', unsafe_allow_html=True)
        with c3:
            name_style = "text-decoration:line-through;color:#555f72" if checked else "color:#e2e8f0"
            st.markdown(f"""
            <div style="{name_style};font-size:14px;font-weight:500;padding-top:4px">{task['name']}</div>
            <div style="font-size:11px;color:#8892a4">{task['meta']}</div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div style="padding-top:6px"><span class="tag {task["tag_class"]}">{task["tag"]}</span></div>', unsafe_allow_html=True)
        with c5:
            if not checked:
                if st.button(T("start"), key=f"start_{i}"):
                    st.session_state.tokens += 10
                    st.session_state.tokens_today += 10
                    st.toast(f"🪙 +10 tokens! Starting {task['name']}!", icon="📖")
        st.markdown('<hr style="border:none;border-top:1px solid #2a2f3e;margin:2px 0">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Revision due today
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T("revision_today")}</div>', unsafe_allow_html=True)
    for r in REVISIONS:
        rc = r["ret_color"]
        st.markdown(f"""
        <div class="rev-item">
            <div style="font-size:22px;width:38px;text-align:center">{r['icon']}</div>
            <div style="flex:1">
                <div style="font-size:13px;font-weight:600;color:#e2e8f0">{r['name']}</div>
                <div style="font-size:11px;color:#8892a4;margin-top:2px">{r['meta']}</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:15px;font-weight:700;color:{rc}">{r['retention']}%</div>
                <div style="font-size:10px;color:#8892a4">{T('retention')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: REVISION
# ═══════════════════════════════════════════════
elif page == T("nav_revision"):

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T("spaced_rep")}</div>', unsafe_allow_html=True)

    for r in REVISIONS:
        rc = r["ret_color"]
        interval_color = "#f87171" if r["interval"] == "1-day" else "#fbbf24" if r["interval"] == "3-day" else "#4ade80"
        st.markdown(f"""
        <div class="rev-item">
            <div style="font-size:22px;width:38px;text-align:center">{r['icon']}</div>
            <div style="flex:1">
                <div style="font-size:13px;font-weight:600;color:#e2e8f0">{r['name']}</div>
                <div style="font-size:11px;color:#8892a4;margin-top:2px">{r['meta']}</div>
            </div>
            <div style="margin-right:12px">
                <span style="background:#1f2435;color:{interval_color};border:1px solid {interval_color}44;
                             font-size:10px;padding:3px 9px;border-radius:10px">{r['interval']}</span>
            </div>
            <div style="text-align:right">
                <div style="font-size:15px;font-weight:700;color:{rc}">{r['retention']}%</div>
                <div style="font-size:10px;color:#8892a4">{T('retention')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T("rep_rules")}</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #f87171"><div style="font-weight:600;color:#f87171;margin-bottom:4px;font-size:13px">Score &lt; 50 · 1-day</div><div style="font-size:12px;color:#8892a4">Very weak — daily reinforcement needed</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #fbbf24"><div style="font-weight:600;color:#fbbf24;margin-bottom:4px;font-size:13px">Score 50–74 · 3-day</div><div style="font-size:12px;color:#8892a4">Medium — steady consolidation</div></div>', unsafe_allow_html=True)
    with r3:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #00c9a7"><div style="font-weight:600;color:#00c9a7;margin-bottom:4px;font-size:13px">Score 75+ · 7-day</div><div style="font-size:12px;color:#8892a4">Strong — long-term retention</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: PROGRESS
# ═══════════════════════════════════════════════
elif page == T("nav_progress"):

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T("mastery_gain"),  "+14%", delta="+14%")
    m2.metric(T("consistency"),   "86%")
    m3.metric(T("avg_quiz"),      "72%",  delta="-2%")
    m4.metric(T("avg_speed"),     "2.1 min")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("mastery_trend")}</div>', unsafe_allow_html=True)
        fig = go.Figure()
        trend = MASTERY_TREND
        fig.add_scatter(x=trend["weeks"], y=trend["overall"],     name="Overall",     line=dict(color="#00c9a7", width=2), fill="tozeroy", fillcolor="rgba(0,201,167,0.08)")
        fig.add_scatter(x=trend["weeks"], y=trend["chemistry"],   name="Chemistry",   line=dict(color="#f472b6", width=2))
        fig.add_scatter(x=trend["weeks"], y=trend["programming"], name="Programming", line=dict(color="#38bdf8", width=2))
        fig.add_scatter(x=trend["weeks"], y=trend["physics"],     name="Physics",     line=dict(color="#a78bfa", width=2))
        fig.update_layout(**PLOT_LAYOUT, height=250,
                          xaxis=dict(**GRID_STYLE),
                          yaxis=dict(**GRID_STYLE, range=[20, 100]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("quiz_acc")}</div>', unsafe_allow_html=True)
        qa = QUIZ_ACCURACY
        fig = go.Figure(go.Bar(
            x=qa["accuracy"], y=qa["subjects"],
            orientation="h",
            marker_color=qa["colors"],
            text=[f"{v}%" for v in qa["accuracy"]],
            textposition="outside",
            textfont=dict(color="#8892a4", size=10),
        ))
        fig.update_layout(**PLOT_LAYOUT, height=250,
                          xaxis=dict(**GRID_STYLE, range=[0, 105]),
                          yaxis=dict(**GRID_STYLE))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T("coach_insights")}</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #4ade80;font-size:12px;color:#e2e8f0;line-height:1.6;margin-bottom:10px"><strong style="color:#4ade80">Programming ↑ 88%</strong> — Best subject. Keep it maintained with weekly revision.</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #fbbf24;font-size:12px;color:#e2e8f0;line-height:1.6"><strong style="color:#fbbf24">Physics at 71%</strong> — Good, but Newton\'s Laws needs revision — 14 days overdue.</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #4ade80;font-size:12px;color:#e2e8f0;line-height:1.6;margin-bottom:10px"><strong style="color:#4ade80">14-day streak</strong> — Excellent! You\'ve studied every single day this fortnight.</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #f87171;font-size:12px;color:#e2e8f0;line-height:1.6"><strong style="color:#f87171">Chemistry critical (28%)</strong> — Organic Reactions needs urgent daily practice starting today.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: AI COACH
# ═══════════════════════════════════════════════
elif page == T("nav_coach"):

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "ai", "content": "Hi! I've analysed your data. Chemistry (28%) is your biggest risk right now. Organic Reactions needs daily attention. Want me to build a focused rescue plan?"}
        ]

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-header">{T("coach_online")}</div>', unsafe_allow_html=True)

    chat_html = '<div style="padding:14px;min-height:200px;max-height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:8px">'
    for msg in st.session_state.messages:
        cls = "msg-ai" if msg["role"] == "ai" else "msg-user"
        content = msg["content"].replace("\n", "<br>")
        chat_html += f'<div class="{cls}" style="white-space:pre-line">{content}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"**{T('quick_q')}**")
    qcols = st.columns(4)
    quick_qs = list(AI_RESPONSES.keys())
    for col, q in zip(qcols, quick_qs):
        with col:
            if st.button(q, key=f"quick_{q[:20]}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.messages.append({"role": "ai",   "content": AI_RESPONSES[q]})
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        fc1, fc2 = st.columns([5, 1])
        with fc1:
            user_input = st.text_input(T("ask_placeholder"), placeholder="e.g. Why is Chemistry weak?", label_visibility="collapsed")
        with fc2:
            submitted = st.form_submit_button(T("send"), use_container_width=True)

    if submitted and user_input.strip():
        reply = AI_RESPONSES.get(
            user_input.strip(),
            "Based on your performance data: Chemistry needs the most attention (28% mastery). "
            "Your Programming skills are strong at 88%. Shall I create a balanced revision schedule?"
        )
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        st.session_state.messages.append({"role": "ai",   "content": reply})
        st.rerun()

    if st.button(T("clear_chat")):
        st.session_state.messages = [
            {"role": "ai", "content": "Hi! I'm your SmartStudy AI Coach. Ask me anything about your study plan, weak topics, or progress!"}
        ]
        st.rerun()


# ═══════════════════════════════════════════════
# PAGE: TOKENS
# ═══════════════════════════════════════════════
elif page == T("nav_tokens"):

    # ── Token balance hero ──────────────────────
    st.markdown(f"""
    <div class="dash-card" style="background:linear-gradient(135deg,#1a1e2a,#1f2435);border-color:#fbbf2433">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px">
            <div>
                <div class="section-label" style="color:#fbbf24aa">{T('token_title')}</div>
                <div style="font-size:52px;font-weight:700;color:#fbbf24;line-height:1">
                    🪙 {st.session_state.tokens:,}
                </div>
                <div style="font-size:13px;color:#8892a4;margin-top:4px">
                    +{st.session_state.tokens_today} {T('tokens_earned')} &nbsp;·&nbsp;
                    <span style="color:#4ade80">Rank #4 on leaderboard</span>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;min-width:240px">
                <div style="background:#1a1e2a;border:1px solid #2a2f3e;border-radius:10px;padding:12px;text-align:center">
                    <div style="font-size:10px;color:#8892a4;margin-bottom:4px">{T('total_earned')}</div>
                    <div style="font-size:20px;font-weight:700;color:#e2e8f0">7,290</div>
                </div>
                <div style="background:#1a1e2a;border:1px solid #2a2f3e;border-radius:10px;padding:12px;text-align:center">
                    <div style="font-size:10px;color:#8892a4;margin-bottom:4px">{T('redeemed')}</div>
                    <div style="font-size:20px;font-weight:700;color:#f87171">3,650</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs: Earn / Store / Leaderboard / Badges ──
    tab1, tab2, tab3, tab4 = st.tabs([
        f"⚡ {T('earn_tokens')}",
        f"🛒 {T('rewards_store')}",
        f"🏆 {T('leaderboard')}",
        f"🎖 {T('your_badges')}",
    ])

    # TAB 1 — How to earn
    with tab1:
        col_earn, col_activity = st.columns([1.1, 0.9])

        with col_earn:
            st.markdown('<div class="dash-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-label">{T("earn_tokens")}</div>', unsafe_allow_html=True)
            for rule in TOKEN_RULES:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid #2a2f3e">
                    <span style="font-size:18px;width:28px;text-align:center">{rule['icon']}</span>
                    <div style="flex:1;font-size:13px;color:#e2e8f0">{rule['action']}</div>
                    <span style="background:#2a1f06;color:#fbbf24;border:1px solid #fbbf2444;
                                 font-size:12px;font-weight:700;padding:3px 12px;border-radius:20px">
                        +{rule['tokens']} 🪙
                    </span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_activity:
            st.markdown('<div class="dash-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-label">{T("recent_activity")}</div>', unsafe_allow_html=True)
            for act in TOKEN_ACTIVITY:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid #2a2f3e">
                    <div style="flex:1">
                        <div style="font-size:13px;color:#e2e8f0">{act['action']}</div>
                        <div style="font-size:11px;color:#555f72;margin-top:2px">{act['time']}</div>
                    </div>
                    <span style="font-size:14px;font-weight:700;color:{act['color']}">{act['tokens']}</span>
                </div>
                """, unsafe_allow_html=True)

            # Earn button demo
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎯 Simulate completing a task (+10 🪙)", use_container_width=True):
                st.session_state.tokens += 10
                st.session_state.tokens_today += 10
                st.toast("🪙 +10 tokens earned for completing a task!", icon="✅")
                st.rerun()
            if st.button("📝 Simulate passing a quiz (+25 🪙)", use_container_width=True):
                st.session_state.tokens += 25
                st.session_state.tokens_today += 25
                st.toast("🪙 +25 tokens earned for passing a quiz!", icon="📝")
                st.rerun()
            if st.button("🔥 Simulate streak bonus (+100 🪙)", use_container_width=True):
                st.session_state.tokens += 100
                st.session_state.tokens_today += 100
                st.toast("🪙 +100 streak bonus tokens!", icon="🔥")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # TAB 2 — Rewards Store
    with tab2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("rewards_store")}</div>', unsafe_allow_html=True)

        # Group by category
        categories = {}
        for reward in REWARDS_STORE:
            categories.setdefault(reward["category"], []).append(reward)

        for cat, items in categories.items():
            st.markdown(f'<div style="font-size:11px;font-weight:600;color:#555f72;letter-spacing:1px;margin:14px 0 8px;text-transform:uppercase">{cat}</div>', unsafe_allow_html=True)
            cols = st.columns(len(items))
            for col, reward in zip(cols, items):
                with col:
                    can_afford = st.session_state.tokens >= reward["cost"]
                    border_color = "#fbbf2444" if can_afford else "#2a2f3e"
                    st.markdown(f"""
                    <div style="background:#1a1e2a;border:1px solid {border_color};border-radius:12px;
                                padding:16px;text-align:center;margin-bottom:4px">
                        <div style="font-size:28px;margin-bottom:8px">{reward['icon']}</div>
                        <div style="font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:6px">{reward['name']}</div>
                        <div style="font-size:14px;font-weight:700;color:#fbbf24;margin-bottom:10px">
                            🪙 {reward['cost']:,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    btn_label = f"{T('redeem')} ({reward['cost']} 🪙)"
                    if st.button(btn_label, key=f"redeem_{reward['name']}", use_container_width=True, disabled=not can_afford):
                        st.session_state.tokens -= reward["cost"]
                        st.toast(f"✅ Redeemed: {reward['name']}!", icon=reward["icon"])
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 3 — Leaderboard
    with tab3:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("leaderboard")}</div>', unsafe_allow_html=True)

        # Chart
        lb_names   = [e["name"] for e in LEADERBOARD]
        lb_tokens  = [e["tokens"] for e in LEADERBOARD]
        lb_colors  = ["#fbbf24" if "You" in n else "#2a2f3e" for n in lb_names]
        lb_colors[0] = "#ffd700"; lb_colors[1] = "#c0c0c0"; lb_colors[2] = "#cd7f32"

        fig = go.Figure(go.Bar(
            x=lb_tokens, y=lb_names,
            orientation="h",
            marker_color=lb_colors,
            text=[f"🪙 {v:,}" for v in lb_tokens],
            textposition="outside",
            textfont=dict(color="#8892a4", size=11),
        ))
        fig.update_layout(**PLOT_LAYOUT, height=300,
                          xaxis=dict(**GRID_STYLE, range=[0, max(lb_tokens) * 1.2]),
                          yaxis=dict(**GRID_STYLE, autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Table
        for entry in LEADERBOARD:
            is_you = "You" in entry["name"]
            bg = "#1f2a1a" if is_you else "#1a1e2a"
            border = "#4ade8044" if is_you else "#2a2f3e"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;padding:10px 14px;
                        background:{bg};border:1px solid {border};border-radius:10px;margin-bottom:6px">
                <span style="font-size:18px;width:28px;text-align:center">{entry['badge'] or f"#{entry['rank']}"}</span>
                <div style="flex:1;font-size:13px;font-weight:{'600' if is_you else '400'};
                            color:{'#4ade80' if is_you else '#e2e8f0'}">{entry['name']}</div>
                <span style="font-size:11px;color:#8892a4">🔥 {entry['streak']}d</span>
                <span style="font-size:14px;font-weight:700;color:#fbbf24">🪙 {entry['tokens']:,}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 4 — Badges
    with tab4:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{T("your_badges")}</div>', unsafe_allow_html=True)

        badge_cols = st.columns(4)
        for i, badge in enumerate(BADGES):
            with badge_cols[i % 4]:
                earned = badge["earned"]
                bg     = "#1a2a1a" if earned else "#1a1e2a"
                border = "#4ade8066" if earned else "#2a2f3e"
                opacity = "1" if earned else "0.4"
                lock    = "" if earned else "🔒"
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {border};border-radius:12px;
                            padding:16px;text-align:center;margin-bottom:12px;opacity:{opacity}">
                    <div style="font-size:32px;margin-bottom:6px">{badge['icon']}{lock}</div>
                    <div style="font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:4px">{badge['name']}</div>
                    <div style="font-size:11px;color:#8892a4">{badge['desc']}</div>
                    {'<div style="font-size:10px;color:#4ade80;margin-top:6px;font-weight:600">✓ EARNED</div>' if earned else '<div style="font-size:10px;color:#555f72;margin-top:6px">Locked</div>'}
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
