# Coklu Yapay Zeka Konseyi (AI Orkestratoru)

5 farkli yapay zekanin bir araya gelerek (Konsey modu) tartistigi, birbirini denetledigi ve daha kaliteli bir cevap urettigi tasinabilir AI sistemi.

Repo: <GITHUB_REPO_LINKINI_BURAYA_EKLE>

## Neden Bu Proje?

Tek bir model yerine, farkli islerde uzman modelleri bir "orchestration" katmaniyla yonetmek gercek hayatta daha kullanislidir. Bu proje:
- Niyet siniflandirma (routing) yapar
- Farkli model task'larini bir araya getirir
- Yapilandirilabilir bir config ile model degistirmeyi kolaylastirir

## Ozellikler

- Duygu analizi (text classification)
- Niyet anlama (zero-shot classification + keyword fallback)
- Ozetleme
- Ceviri
- Kod uretimi / hata duzeltme (chat completion)
- Arastirma: DuckDuckGo ile arama + model ile sentez
- Konsey modu: 5 model gorus + sentez
- Terminal (CLI) arayuzu
- Web arayuzu (Flask)
- Token guvenligi: `.env` + `.gitignore`

## Konsey Modu (5 AI Mantigi)

Kullanici metninde `konsey` veya `council` gecerse sistem Konsey moduna gecer:

1. Arastirmaci AI: arka plan ve gerekirse web arama baglami
2. Analist AI: mantiksal analiz, riskler, belirsizlikler
3. Elestirmen AI: karsi arguman, zayif noktalar
4. Sentezleyici AI: gorusleri birlestirip kapsamli cevap
5. Denetleyici AI: tutarlilik ve guvenlik kontrolu

Not: Bazi modeller lisans/izin veya provider nedeniyle erisilemeyebilir. Bu durumda sistem ilgili uyeyi atlayip kalan cevaplarla sentez yapar.

## Kullanilan Modeller (Hugging Face)

- Gemma 2 9B: `google/gemma-2-9b-it`
- Llama 3.1 8B: `meta-llama/Llama-3.1-8B-Instruct`
- Mistral 7B: `mistralai/Mistral-7B-Instruct-v0.3`
- Qwen2 7B: `Qwen/Qwen2.5-7B-Instruct`
- Phi-3 Medium: `microsoft/Phi-3-medium-128k-instruct`

## Kullanilan Motor / API (Nasil Cagiriyor?)

Bu projede modeller **yerel olarak indirilmiyor**. Istekler, Hugging Face'in **Inference Providers** altyapisi uzerinden gonderiliyor.

- Python tarafinda `huggingface_hub.InferenceClient(provider="auto", token=HF_TOKEN)` kullanilir.
- Kullanilan temel cagrilar:
  - `chat_completion` (genel sohbet + kod uretimi / hata duzeltme)
  - `summarization` (ozet)
  - `translation` (ceviri)
  - `zero_shot_classification` (niyet / routing)
  - `text_classification` (duygu analizi)

Not: Bu yapi internet baglantisi gerektirir ve metin icerigi ilgili provider'a gonderilir (token ile yetkilendirilmis sekilde).

## Hizli Baslangic (Windows)

1. Kurulum:

```bat
install.bat
```

2. Token ayari:

- `.env.example` dosyasini `.env` yap
- Icine token ekle:

```env
HF_TOKEN=your_hugging_face_token_here
```

Not: Token olustururken "Inference Providers" cagrilarina izin veren secenek acik olmali. Aksi halde chat tabanli modeller 403 yetki hatasi verebilir.

3. Calistir:

- CLI:

```bat
run.bat
```

- Web UI:

```bat
run_web.bat
```

Tarayici:
`http://127.0.0.1:7860/`

Alternatif UI (dosya):
`index.html` (calismasi icin `run_web.bat` acik olmali)

## Kullanim Ornekleri

```text
Bu metni ozetle: ...
```

```text
Su metni cevir: ...
```

```text
Bu Python hatasini duzelt: TypeError: ...
```

```text
Python ile JSON okuyan temiz bir fonksiyon yaz.
```

```text
Hugging Face Inference Providers nedir arastir.
```

## Mimari (Ozet)

```text
Kullanici metni
  -> Router (intent + sentiment)
  -> Model dispatch (summarize/translate/chat/research)
  -> Tek cevap (intent + sentiment + answer)
```

## Model Plani (config.yaml)

Modeller `config.yaml` icinde tanimli. Varsayilan plan:

- sentiment: `savasy/bert-base-turkish-sentiment-cased`
- intent: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`
- summarization: `csebuetnlp/mT5_multilingual_XLSum`
- translation: `facebook/nllb-200-distilled-600M`
- coding + general chat: `Qwen/Qwen2.5-Coder-7B-Instruct`
- council members: `google/gemma-2-9b-it`, `meta-llama/Llama-3.1-8B-Instruct`, `mistralai/Mistral-7B-Instruct-v0.3`, `Qwen/Qwen2.5-7B-Instruct`, `microsoft/Phi-3-medium-128k-instruct`

Not: Bazi modeller her provider uzerinden acik olmayabilir. Bu durumda `config.yaml` uzerinden model degistirmek yeterli.

## Proje Yapisi

```text
multi-ai-orchestrator/
  app.py
  web_app.py
  index.html
  config.yaml
  requirements.txt
  orchestrator/
    cli.py
    hf_client.py
    research.py
    router.py
    settings.py
  templates/
    index.html
  static/
    app.js
    styles.css
  tests/
```

## Guvenlik

- Gercek token sadece `.env` icinde tutulur.
- `.env` `.gitignore` icindedir; GitHub'a yuklenmez.
- README veya kaynak kod icine token yazilmaz.

## Troubleshooting

- `.env icinde HF_TOKEN bulunamadi`:
  `.env` dosyasi yoktur veya bosdur. `.env.example` -> `.env` yapip token ekle.

- `403 Forbidden / insufficient permissions`:
  Token izinlerinde "Inference Providers" cagrisi kapali olabilir. Yeni token olusturup dogru izni ac.

- `404 Not Found`:
  Secili model bu endpoint/provider uzerinden acik olmayabilir. `config.yaml` icinde modeli degistir.

- `Arastirma calismiyor`:
  DuckDuckGo arama kisitlanmis olabilir. Farkli bir agda dene veya `max_results` dusur.

## Lisans

MIT (bkz. `LICENSE`)
