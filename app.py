import streamlit as st
import os
import io
import google.generativeai as genai
from PIL import Image

# --- কনফিগারেশন এবং নিরাপত্তা সতর্কতা ---
# ঝুঁকি সতর্কতা (এই অংশটি প্রফেশনাল অ্যাপে বাধ্যতামূলক)
ST_RISK_WARNING = """
<div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
    <strong>ঝুঁকি সতর্কতা:</strong> বাইনারি অপশন ট্রেডিং, বিশেষ করে OTC (Over-The-Counter) মার্কেট অত্যন্ত ঝুঁকিপূর্ণ। 
    কোনো AI বা সিস্টেম ১০০% সঠিক সিগন্যাল দিতে পারে না। এই টুলটি শুধুমাত্র একটি সহায়ক অ্যানালাইসিস টুল। 
    দয়া করে নিজের গবেষণা করুন এবং ততটুকুই ইনভেস্ট করুন যা হারানোর ক্ষমতা আপনার আছে।
</div>
"""

# Gemini API কী সেট করুন (আপনার নিজের API কী দিয়ে এটি প্রতিস্থাপন করুন)
# এটি কীভাবে পাবেন, তা জানতে https://ai.google.dev/ দেখুন
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"  # <--- আপনার API কী এখানে দিন
if not os.environ["GOOGLE_API_KEY"] or os.environ["GOOGLE_API_KEY"] == "YOUR_GEMINI_API_KEY_HERE":
    st.error("দয়া করে আপনার Gemini API কী সেট করুন। Google AI Studio থেকে এটি পেতে পারেন।")
    st.stop()

# Gemini Vision মডেল সেটআপ
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro-vision')

# --- পেজ কনফিগারেশন ---
st.set_page_config(
    page_title="প্রফেশনাল AI ট্রেডিং সিগন্যাল বোট | Bangladesh",
    page_icon="📈",
    layout="wide"
)

# --- সিগন্যাল ইমেজ ডাউনলোড (প্রদর্শনের জন্য) ---
def load_signal_image(type):
    if type == "CALL":
        # এখানে image_0.png এর URL বা লোকাল পাথ ব্যবহার করুন
        # (ডেমোর জন্য আমি সরাসরি URL বা লোকাল পাথ দিচ্ছি না, আপনি যেখানে কোড রান করবেন সেখানে রাখলে সরাসরি path ব্যবহার করতে পারেন)
        # return Image.open('path_to_image_0.png')
        pass # replace with actual load
    elif type == "PUT":
        # return Image.open('path_to_image_1.png')
        pass # replace with actual load

# --- Gemini Vision API কল ফাংশন ---
def get_ai_signal(prompt, image):
    try:
        if image:
            response = model.generate_content([prompt, image])
            return response.text
        else:
            return "কোনো চার্ট ইমেজ আপলোড করা হয়নি।"
    except Exception as e:
        return f"অ্যানালাইসিসের সময় ত্রুটি: {str(e)}"

# --- প্রধান অ্যাপ কাঠামো ---
def main():
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>📈 প্রফেশনাল AI ট্রেডিং সিগন্যাল বোট (OTC মার্কেট)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>বাংলাদেশী ট্রেডারদের জন্য ডিজাইন করা উন্নত চার্ট অ্যানালাইসিস টুল</p>", unsafe_allow_html=True)
    
    st.markdown(ST_RISK_WARNING, unsafe_allow_html=True)

    # --- সাইডবার (সিলেকশন প্যানেল) ---
    st.sidebar.header("সেটিংস")

    # ব্রোকার সিলেকশন
    brokers = ["Quotex", "Pocket Option", "Binomo", "IQ Option", "Expert Option", "Binola"]
    selected_broker = st.sidebar.selectbox("আপনার ব্রোকার বেছে নিন:", brokers)

    # OTC মার্কেট পেয়ার সিলেকশন (বিস্তারিত তালিকা)
    otc_assets = [
        "EUR/USD (OTC)", "EUR/GBP (OTC)", "EUR/JPY (OTC)",
        "USD/EGP (OTC)", "USD/COP (OTC)", "USD/ZAR (OTC)",
        "USD/NZD (OTC)", "USD/BDT (OTC)", "USD/CAD (OTC)",
        "USD/BRL (OTC)", "AUD/USD (OTC)", "GBP/USD (OTC)",
        "JPY/USD (OTC)", "CHF/USD (OTC)", "NZD/USD (OTC)"
    ]
    selected_asset = st.sidebar.selectbox("ট্রেডিং পেয়ার (OTC):", otc_assets)

    st.sidebar.info(f"আপনি বর্তমানে **{selected_broker}** ব্রোকারে **{selected_asset}** পেয়ারে ট্রেড করার জন্য প্রস্তুতি নিচ্ছেন।")

    # --- প্রধান কন্টেন্ট এলাকা ---
    
    # স্ক্রিনশট আপলোড সেকশন
    st.subheader("📊 মার্কেট স্ক্রিনশট আপলোড করুন")
    
    # ফাইল আপলোডারের পাশে ক্রস চিহ্নের মতো ডিলিট অপশন স্ট্রিমলিট ডিফল্টভাবেই দেয়।
    # ইউজার চাইলে আপলোড করা ফাইল ডিলিট বা প্রতিস্থাপন করতে পারে।
    uploaded_file = st.file_uploader("আপনার ট্রেডিং চার্টের পরিষ্কার স্ক্রিনশট (JPEG/PNG) আপলোড করুন। নিশ্চিত করুন যে বর্তমান ক্যান্ডেল এবং সাপোর্ট/রেজিস্ট্যান্স লেভেলগুলো দেখা যাচ্ছে।", type=["jpg", "jpeg", "png"])
    
    current_image = None
    if uploaded_file is not None:
        # আপলোড করা ইমেজ লোড করুন
        current_image = Image.open(uploaded_file)
        # ইমেজ প্রদর্শন করুন (এটি ছোট আকারে দেখানো হচ্ছে)
        st.image(current_image, caption='আপলোড করা চার্ট', use_column_width=False, width=400)
        
        # ফাইল ডিলিট/রিপ্লেস করার ডিফল্ট স্ট্রিমলিট UI ব্যবহার হচ্ছে। 'Remove' বাটনে ক্লিক করলে এটি চলে যাবে।
        
    st.markdown("---")

    # --- অ্যানালাইসিস এবং সিগন্যাল সেকশন ---
    st.subheader("🔍 AI অ্যানালাইসিস এবং সিগন্যাল")

    # অ্যানালাইসিস বাটন
    analysis_button = st.button("এনালাইসিস")

    if analysis_button:
        if current_image is not None:
            with st.spinner(f"AI আপনার {selected_asset} চার্ট বিশ্লেষণ করছে..."):
                # Gemini Vision-এর জন্য প্রম্পট
                signal_prompt = f"""
                You are a professional Binary Options price action analyst focusing on {selected_asset} market on the {selected_broker} broker.
                Analyze the provided candlestick chart screenshot. Look for:
                1. Main market trend.
                2. Key Support and Resistance levels.
                3. High-probability Candlestick Patterns (like Hammer, Shooting Star, Bullish Engulfing, etc.) near key levels.
                4. Indicators (if any are visible and clear, mention them briefly, else ignore).
                
                Based on this detailed analysis, predict the most likely direction for the VERY NEXT ONE-MINUTE CANDLE. 
                Your response must be in strict professional format and include:
                - Predominant Direction (UP or DOWN or NEUTRAL)
                - Rationale (Explanation of findings like "Hammer pattern identified at strong support level", "Bearish engulfing seen at resistance").
                - Confidence Level (Estimate probability based on price action alone, never state 100%, but give a realistic assessment like "High (80%)+", "Medium (70-80%)").
                """
                
                # AI সিগন্যাল এবং অ্যানালাইসিস পান
                ai_response = get_ai_signal(signal_prompt, current_image)
                
                # --- সিগন্যাল রেসপন্স পার্সিং (সরলীকৃত) ---
                direction = "NEUTRAL"
                if "Direction: UP" in ai_response:
                    direction = "UP"
                elif "Direction: DOWN" in ai_response:
                    direction = "DOWN"

                # --- সিগন্যাল প্রদর্শন ---
                col1, col2 = st.columns([1, 3])

                with col1:
                    if direction == "UP":
                        # call_img = load_signal_image("CALL") # লোড ফাংশন সেট করা হলে
                        # st.image(call_img, width=150)
                        st.markdown("<div style='background-color: #4CAF50; color: white; padding: 15px; text-align: center; border-radius: 5px; font-weight: bold; font-size: 20px;'>CALL (আপ)</div>", unsafe_allow_html=True)
                    elif direction == "DOWN":
                        # put_img = load_signal_image("PUT") # লোড ফাংশন সেট করা হলে
                        # st.image(put_img, width=150)
                        st.markdown("<div style='background-color: #F44336; color: white; padding: 15px; text-align: center; border-radius: 5px; font-weight: bold; font-size: 20px;'>PUT (ডাউন)</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color: #ff9800; color: white; padding: 15px; text-align: center; border-radius: 5px; font-weight: bold; font-size: 20px;'>অনিশ্চিত</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**ট্রেডিং জোড়া:** {selected_asset}")
                    st.markdown(f"**ব্রোকার:** {selected_broker}")
                    st.markdown("---")
                    st.markdown("### বিস্তারিত AI অ্যানালাইসিস:")
                    st.markdown(ai_response)

        else:
            st.error("দয়া করে 'এনালাইসিস' বাটনে ক্লিক করার আগে একটি চার্টের স্ক্রিনশট আপলোড করুন।")

    # --- ফুটার ---
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 12px;'>এটি একটি এডুকেশনাল প্রোটোটাইপ। আসল ট্রেডিংয়ে ঝুঁকি থাকে। দায়িত্ব নিজের।</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
