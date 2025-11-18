# migration_to_new_services.py
# This file documents the migration plan, env changes and basic testing steps.

migration_text = r'''
=================================================================
Migration Plan to OpenAI and ElevenLabs Services
=================================================================

Add these environment variables to .env:
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=elevenlabs-...
ELEVENLABS_VOICE_ID=your-voice-id
SERPAPI_API_KEY=serpapi-... (optional)

Install dependencies:
pip install openai python-dotenv requests serpapi

Files added:
- services/openai_client.py
- services/image_gen.py
- services/elevenlabs_tts.py
- services/search_serpapi.py (optional)

How to test:
- From python REPL, import and call generate_script, generate_storyboard_images and tts_generate_wav.

Example testing:
  from services.openai_client import generate_script, create_image
  from services.elevenlabs_tts import tts_generate_wav
  from services.image_gen import generate_storyboard_images
  
  # Test script generation
  script = generate_script("AI technology", length_seconds=60)
  print(script)
  
  # Test image generation
  img_url = create_image("futuristic AI robot")
  print(img_url)
  
  # Test TTS
  tts_generate_wav("Hello world", output_path="test.wav")

=================================================================
Search patterns to find old provider usage:
=================================================================

Run these commands locally to find code that needs migration:

1. Find all old provider API keys and imports:
   grep -RIn "GROQ_API_KEY\|TOGETHER_API_KEY\|TAVILY_API_KEY\|F5-TTS\|F5_TTS\|together.ai\|groq\|tavily" .

2. Find specific function calls to old providers:
   grep -RIn "make_groq_completion\|TogetherClient\|together_api\|tavily_client\|f5_tts\|AsyncGroq\|Together(" .

3. Find Together AI image generation:
   grep -RIn "together.images\|black-forest-labs/FLUX" .

4. Find Tavily search usage:
   grep -RIn "tavily.com/search\|WebSearchTool" .

=================================================================
Recommended replacement mappings:
=================================================================

OLD PROVIDER                    → NEW SERVICE
--------------------------------------------------------------------
AsyncGroq (LLM)                 → services.openai_client.chat_completion
Together (images)               → services.openai_client.create_image
TogetherAI FLUX                 → services.openai_client.create_image
Tavily search                   → services.search_serpapi.serp_search
F5-TTS                          → services.elevenlabs_tts.tts_generate_wav

Example replacements:

1. Replace Groq chat completions:
   OLD: client = AsyncGroq(api_key=groq_api_key)
        stream = await client.chat.completions.create(...)
   NEW: from services.openai_client import chat_completion
        result = chat_completion(messages=[...])

2. Replace Together AI image generation:
   OLD: client = Together(api_key=together_api_key)
        response = client.images.generate(...)
   NEW: from services.openai_client import create_image
        url = create_image(prompt="...")

3. Replace Tavily search:
   OLD: tavily_api.search(query, ...)
   NEW: from services.search_serpapi import serp_search, summarize_search_results
        results = serp_search(query)
        summary = summarize_search_results(results)

4. Replace F5-TTS:
   OLD: F5-TTS command line generation
   NEW: from services.elevenlabs_tts import tts_generate_wav
        tts_generate_wav(text, output_path="audio.wav")

=================================================================
'''

print(migration_text)
