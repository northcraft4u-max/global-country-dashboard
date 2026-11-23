import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(
    page_title="Global Country Intelligence",
    page_icon="🌍",
    layout="wide"
)

NEWS_API_KEY = "5e38db7f5b2d43579dd6d28f981d0fdb"
WEATHER_API_KEY = "26631f0f41b95fb9f5ac0df9a8f43c92"

CURRENCIES = [
    "USD", "CAD", "EUR", "GBP", "INR", "AED",
    "JPY", "AUD", "BRL", "CHF", "SGD", "MXN"
]

COUNTRIES = {
    "Canada": {
        "code": "ca",
        "capital": "Ottawa",
        "cities": ["Ottawa", "Toronto", "Vancouver", "Montreal", "Calgary", "Edmonton"],
        "currency": "CAD",
        "flag": "https://flagcdn.com/w320/ca.png",
        "official": "Canada",
        "region": "Americas",
        "subregion": "North America",
        "population": "41,288,599",
        "languages": "English, French",
        "timezone": "UTC-08:00 to UTC-03:30"
    },
    "United States": {
        "code": "us",
        "capital": "Washington",
        "cities": ["Washington", "New York", "Los Angeles", "Chicago", "Houston", "Miami"],
        "currency": "USD",
        "flag": "https://flagcdn.com/w320/us.png",
        "official": "United States of America",
        "region": "Americas",
        "subregion": "North America",
        "population": "340,110,988",
        "languages": "English",
        "timezone": "UTC-12:00 to UTC+10:00"
    },
    "United Kingdom": {
        "code": "gb",
        "capital": "London",
        "cities": ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Liverpool"],
        "currency": "GBP",
        "flag": "https://flagcdn.com/w320/gb.png",
        "official": "United Kingdom of Great Britain and Northern Ireland",
        "region": "Europe",
        "subregion": "Northern Europe",
        "population": "68,265,209",
        "languages": "English",
        "timezone": "UTC+00:00"
    },
    "India": {
        "code": "in",
        "capital": "New Delhi",
        "cities": ["New Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Kolkata"],
        "currency": "INR",
        "flag": "https://flagcdn.com/w320/in.png",
        "official": "Republic of India",
        "region": "Asia",
        "subregion": "Southern Asia",
        "population": "1,417,492,000",
        "languages": "Hindi, English",
        "timezone": "UTC+05:30"
    },
    "United Arab Emirates": {
        "code": "ae",
        "capital": "Abu Dhabi",
        "cities": ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Ras Al Khaimah"],
        "currency": "AED",
        "flag": "https://flagcdn.com/w320/ae.png",
        "official": "United Arab Emirates",
        "region": "Asia",
        "subregion": "Western Asia",
        "population": "10,678,556",
        "languages": "Arabic",
        "timezone": "UTC+04:00"
    },
    "Germany": {
        "code": "de",
        "capital": "Berlin",
        "cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Stuttgart"],
        "currency": "EUR",
        "flag": "https://flagcdn.com/w320/de.png",
        "official": "Federal Republic of Germany",
        "region": "Europe",
        "subregion": "Western Europe",
        "population": "83,491,249",
        "languages": "German",
        "timezone": "UTC+01:00"
    },
    "France": {
        "code": "fr",
        "capital": "Paris",
        "cities": ["Paris", "Lyon", "Marseille", "Nice", "Toulouse", "Bordeaux"],
        "currency": "EUR",
        "flag": "https://flagcdn.com/w320/fr.png",
        "official": "French Republic",
        "region": "Europe",
        "subregion": "Western Europe",
        "population": "68,516,700",
        "languages": "French",
        "timezone": "UTC+01:00"
    },
    "Japan": {
        "code": "jp",
        "capital": "Tokyo",
        "cities": ["Tokyo", "Osaka", "Kyoto", "Yokohama", "Sapporo", "Fukuoka"],
        "currency": "JPY",
        "flag": "https://flagcdn.com/w320/jp.png",
        "official": "Japan",
        "region": "Asia",
        "subregion": "Eastern Asia",
        "population": "123,753,041",
        "languages": "Japanese",
        "timezone": "UTC+09:00"
    },
    "Australia": {
        "code": "au",
        "capital": "Canberra",
        "cities": ["Canberra", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "currency": "AUD",
        "flag": "https://flagcdn.com/w320/au.png",
        "official": "Commonwealth of Australia",
        "region": "Oceania",
        "subregion": "Australia and New Zealand",
        "population": "27,204,809",
        "languages": "English",
        "timezone": "UTC+05:00 to UTC+10:30"
    },
    "Brazil": {
        "code": "br",
        "capital": "Brasilia",
        "cities": ["Brasilia", "Sao Paulo", "Rio de Janeiro", "Salvador", "Curitiba", "Fortaleza"],
        "currency": "BRL",
        "flag": "https://flagcdn.com/w320/br.png",
        "official": "Federative Republic of Brazil",
        "region": "Americas",
        "subregion": "South America",
        "population": "212,583,750",
        "languages": "Portuguese",
        "timezone": "UTC-05:00 to UTC-02:00"
    },
}


class CountryIntelService:
    def __init__(self, country_name):
        self.country_name = country_name
        self.meta = COUNTRIES[country_name]
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_profile_and_flag(self):
        profile = {
            "official_name": self.meta["official"],
            "region": self.meta["region"],
            "subregion": self.meta["subregion"],
            "population": self.meta["population"],
            "languages": self.meta["languages"],
            "timezones": self.meta["timezone"],
            "flag_bytes": None
        }
        flag_url = self.meta["flag"]

        try:
            url = f"https://restcountries.com/v3.1/alpha/{self.meta['code']}"
            res = requests.get(url, headers=self.headers, timeout=10, verify=False)
            if res.status_code == 200:
                raw = res.json()
                data = raw[0] if isinstance(raw, list) else raw
                profile["official_name"] = data.get("name", {}).get("official", profile["official_name"])
                profile["region"] = data.get("region", profile["region"])
                profile["subregion"] = data.get("subregion", profile["subregion"])
                pop = data.get("population")
                if isinstance(pop, int) and pop > 0:
                    profile["population"] = f"{pop:,}"
                langs = data.get("languages", {})
                if langs:
                    profile["languages"] = ", ".join(langs.values())
                tz = data.get("timezones", [])
                if tz:
                    profile["timezones"] = ", ".join(tz[:2])
                flag_url = data.get("flags", {}).get("png", flag_url)
        except Exception:
            pass

        try:
            img_res = requests.get(flag_url, headers=self.headers, timeout=10, verify=False)
            if img_res.status_code == 200:
                profile["flag_bytes"] = img_res.content
        except Exception:
            pass

        return profile

    def get_exchange_rate(self, from_curr, to_curr):
        if from_curr == to_curr:
            return 1.0
        try:
            url = f"https://www.x-rates.com/calculator/?from={from_curr}&to={to_curr}&amount=1"
            html = requests.get(url, headers=self.headers, timeout=8, verify=False).text
            soup = BeautifulSoup(html, "html.parser")
            rate_str = soup.find("span", class_="ccOutputRslt").get_text()
            return float(rate_str.split()[0].replace(",", ""))
        except Exception:
            return None

    def get_weather_forecast(self, city_name):
        code = self.meta["code"].upper()
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name},{code}&appid={WEATHER_API_KEY}&units=metric"
        try:
            data = requests.get(url, timeout=8).json()
            if "list" not in data:
                return [], data.get("message", "Weather unavailable.")
            rows = []
            for slot in data["list"][:8]:
                rows.append({
                    "Time": slot["dt_txt"],
                    "Temp (°C)": round(slot["main"]["temp"], 1),
                    "Feels Like (°C)": round(slot["main"]["feels_like"], 1),
                    "Humidity (%)": slot["main"]["humidity"],
                    "Condition": slot["weather"][0]["description"].title()
                })
            return rows, None
        except Exception as err:
            return [], str(err)

    def get_news_articles(self):
        code = self.meta["code"]
        top_url = f"https://newsapi.org/v2/top-headlines?country={code}&apiKey={NEWS_API_KEY}"
        try:
            articles = requests.get(top_url, timeout=8).json().get("articles", [])
            if len(articles) < 3:
                search_url = (
                    f"https://newsapi.org/v2/everything?qInTitle={self.country_name}"
                    f"&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
                )
                articles = requests.get(search_url, timeout=8).json().get("articles", articles)
            return articles[:6], None
        except Exception as err:
            return [], str(err)


@st.cache_data(show_spinner="Loading country profile and headlines...")
def fetch_country_core(country_name, time_bucket):
    service = CountryIntelService(country_name)
    profile = service.get_profile_and_flag()
    articles, news_err = service.get_news_articles()
    return {
        "updated_at": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
        "meta": service.meta,
        "profile": profile,
        "articles": articles,
        "news_err": news_err,
    }


@st.cache_data(show_spinner="Fetching live exchange rate...")
def fetch_live_currency(country_name, from_curr, to_curr, time_bucket):
    service = CountryIntelService(country_name)
    forward = service.get_exchange_rate(from_curr, to_curr)
    reverse = service.get_exchange_rate(to_curr, from_curr)
    return {
        "forward": forward,
        "reverse": reverse,
        "checked_at": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    }


@st.cache_data(show_spinner="Fetching city weather forecast...")
def fetch_city_weather(country_name, city_name, time_bucket):
    service = CountryIntelService(country_name)
    rows, err = service.get_weather_forecast(city_name)
    return {
        "rows": rows,
        "err": err,
        "checked_at": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    }


with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    chosen_country = st.selectbox("Choose Country", list(COUNTRIES.keys()), index=0)

    country_cities = COUNTRIES[chosen_country]["cities"]
    chosen_city = st.selectbox(
        "Select City (Weather)",
        country_cities,
        index=0,
        key=f"sidebar_city_{chosen_country}"
    )

    interval_label = st.radio("Auto-Update Interval", ["Every 1 Hour", "Every 2 Hours"], index=0)
    interval_sec = 3600 if interval_label == "Every 1 Hour" else 7200

    if st.button("🔄 Refresh Data Now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


@st.fragment(run_every=3600)
def display_dashboard(country_name, default_city, ttl_seconds, schedule_text):
    bucket = int(datetime.now().timestamp() // ttl_seconds)
    core = fetch_country_core(country_name, bucket)
    meta = core["meta"]
    prof = core["profile"]

    st.title(f"🌍 {country_name} — Country Intelligence")
    st.caption(f"Last Updated: {core['updated_at']}  •  Refresh Schedule: {schedule_text}")

    # Section 1: Country Profile & Custom Currency Converter
    left_col, right_col = st.columns([1.15, 1])

    with left_col:
        with st.container(border=True):
            st.subheader("🏳️ Country Profile")
            flag_col, info_col = st.columns([1, 2])
            with flag_col:
                if prof["flag_bytes"]:
                    st.image(prof["flag_bytes"], use_container_width=True)
            with info_col:
                st.write(f"**Official Name:** {prof['official_name']}")
                st.write(f"**Capital City:** {meta['capital']}")
                st.write(f"**Population:** {prof['population']}")
                st.write(f"**Region:** {prof['region']} ({prof['subregion']})")
                st.write(f"**Languages:** {prof['languages']}")
                st.write(f"**Timezone:** {prof['timezones']}")

    with right_col:
        with st.container(border=True):
            st.subheader("💱 Live Currency Converter")

            default_to = meta["currency"] if meta["currency"] != "USD" else "EUR"
            from_idx = CURRENCIES.index("USD")
            to_idx = CURRENCIES.index(default_to) if default_to in CURRENCIES else 1

            cur_c1, cur_c2 = st.columns(2)
            with cur_c1:
                from_currency = st.selectbox(
                    "From Currency",
                    CURRENCIES,
                    index=from_idx,
                    key=f"from_curr_{country_name}"
                )
            with cur_c2:
                to_currency = st.selectbox(
                    "To Currency",
                    CURRENCIES,
                    index=to_idx,
                    key=f"to_curr_{country_name}"
                )

            fx = fetch_live_currency(country_name, from_currency, to_currency, bucket)
            rate = fx["forward"]
            rev_rate = fx["reverse"]

            if rate is not None:
                m1, m2 = st.columns(2)
                m1.metric(f"1 {from_currency} → {to_currency}", f"{rate:,.4f}")
                m2.metric(
                    f"1 {to_currency} → {from_currency}",
                    f"{rev_rate:,.4f}" if rev_rate is not None else "N/A"
                )

                amount = st.number_input(
                    f"Amount ({from_currency})",
                    min_value=1.0,
                    value=100.0,
                    step=10.0,
                    key=f"amt_{country_name}_{from_currency}_{to_currency}"
                )
                st.success(f"{amount:,.2f} {from_currency} = {amount * rate:,.2f} {to_currency}")

                with st.expander("Inspect Live JSON Payload"):
                    st.json({
                        "input_currency": from_currency,
                        "output_currency": to_currency,
                        "rate": rate,
                        "timestamp": fx["checked_at"]
                    })
            else:
                st.warning("Live currency rate temporarily unavailable.")

    # Section 2: 24-Hour Weather Forecast with City Selector
    with st.container(border=True):
        w_head_col, w_city_col = st.columns([2, 1])
        with w_head_col:
            st.subheader(f"🌤️ 24-Hour Weather Forecast")
        with w_city_col:
            city_options = meta["cities"]
            default_city_idx = city_options.index(default_city) if default_city in city_options else 0
            active_city = st.selectbox(
                "Main City",
                city_options,
                index=default_city_idx,
                key=f"card_city_{country_name}_{default_city}"
            )

        weather_data = fetch_city_weather(country_name, active_city, bucket)

        if weather_data["rows"]:
            first_slot = weather_data["rows"][0]
            wk1, wk2, wk3 = st.columns(3)
            wk1.metric(f"{active_city} Temp", f"{first_slot['Temp (°C)']} °C")
            wk2.metric("Feels Like", f"{first_slot['Feels Like (°C)']} °C")
            wk3.metric("Condition", first_slot["Condition"])

            df_weather = pd.DataFrame(weather_data["rows"])
            st.dataframe(df_weather, use_container_width=True, hide_index=True)

            log_lines = "\n".join(
                f"{r['Time']}, {r['Temp (°C)']}C, {r['Condition']}" for r in weather_data["rows"]
            )
            st.download_button(
                label=f"📥 Download {active_city} Weather Log (.txt)",
                data=log_lines,
                file_name=f"{active_city.lower().replace(' ', '_')}_weather.txt",
                mime="text/plain"
            )
        else:
            st.warning(f"Weather unavailable for {active_city}: {weather_data['err']}")

    # Section 3: Top News Headlines
    st.subheader(f"📰 Latest News — {country_name}")
    if core["articles"]:
        cols = st.columns(2)
        for i, art in enumerate(core["articles"]):
            with cols[i % 2]:
                with st.container(border=True):
                    title = art.get("title") or "Untitled Article"
                    desc = art.get("description") or "No summary available."
                    source = art.get("source", {}).get("name", "News")
                    link = art.get("url", "#")

                    st.markdown(f"**{title}**")
                    st.caption(f"Source: {source}")
                    st.write(desc[:160] + ("..." if len(desc) > 160 else ""))
                    st.markdown(f"[Read Article →]({link})")
    else:
        st.warning(f"No news returned: {core['news_err']}")


display_dashboard(chosen_country, chosen_city, interval_sec, interval_label)