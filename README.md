# 🎂 Tug'ilgan Kun Bot — O'rnatish Qo'llanmasi

## 1-qadam: BotFather dan token olish
1. Telegramda `@BotFather` ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: `MyGroupBirthdayBot`)
4. Sizga **TOKEN** beriladi — uni saqlab qo'ying

## 2-qadam: GROUP_ID olish
1. Botni gruppangizga qo'shing (admin qiling)
2. Gruppada `/start` yoki `/check` yozing
3. Brauzerda bu linkni oching:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. `"chat":{"id": -1001234567890}` — mana shu raqam GROUP_ID

## 3-qadam: Railway ga deploy qilish (BEPUL)

### GitHub orqali:
1. `railway.app` ga kiring → GitHub bilan login
2. `New Project` → `Deploy from GitHub repo`
3. Ushbu fayllarni repo ga yuklang
4. `Variables` bo'limiga kiriting:
   - `BOT_TOKEN` = BotFather dan olgan token
   - `GROUP_ID` = -1001234567890 (manfiy son bilan!)
5. Deploy tugmasi → tayyor! ✅

### Render.com orqali (muqobil):
1. `render.com` ga kiring → GitHub bilan login
2. `New` → `Background Worker`
3. Repo ni ulang
4. Environment Variables ga `BOT_TOKEN` va `GROUP_ID` kiriting
5. Deploy ✅

---

## Bot buyruqlari

| Buyruq | Vazifasi |
|--------|----------|
| `/add Ali 15.07` | Ali ni 15-iyul sifatida qo'shish |
| `/list` | Hammani ko'rish |
| `/delete Ali` | Ali ni o'chirish |
| `/check` | Bugun tug'ilgan kun bormi? |

## Eslatma
Bot har kuni **soat 09:00 da** (O'zbekiston vaqti) gruppaga avtomatik tabrik yuboradi.
