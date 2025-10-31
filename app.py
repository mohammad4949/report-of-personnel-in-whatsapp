import os
from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# تنظیمات از محیط
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

@app.route('/')
def home():
    return jsonify({
        "status": "active", 
        "message": "سرویس واتس‌اپ فعال است ✅",
        "service": "WhatsApp Reporter"
    })

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    try:
        incoming_msg = request.values.get('Body', '').lower()
        from_number = request.values.get('From', '')
        
        print(f"پیام از {from_number}: {incoming_msg}")
        
        # پاسخ ساده
        if 'سلام' in incoming_msg:
            response = "👋 سلام! به بات گزارش‌گیری خوش آمدید\n\n📊 برای شروع از 'گزارش' استفاده کنید"
        elif 'گزارش' in incoming_msg:
            response = "📈 سیستم گزارش‌گیری آماده است\n\n🔧 به زودی قابلیت‌های کامل اضافه می‌شود"
        else:
            response = "❌ دستور نامعتبر\n\n💡 از 'سلام' یا 'گزارش' استفاده کنید"
        
        # ارسال پاسخ
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_='whatsapp:+14155238886',
            body=response,
            to=from_number
        )
        
        return 'OK', 200
        
    except Exception as e:
        print(f"خطا: {e}")
        return 'ERROR', 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
