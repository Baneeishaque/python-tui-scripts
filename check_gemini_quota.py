#!/usr/bin/env python3
import os
import sys
import datetime
import argparse
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python versions < 3.9
    from backports.zoneinfo import ZoneInfo
import google.generativeai as genai
from google.api_core import exceptions

def get_ist_time(dt_utc):
    """Converts a UTC datetime to IST."""
    ist = ZoneInfo('Asia/Kolkata')
    return dt_utc.astimezone(ist)

def calculate_reset_info():
    """Calculates the next reset time in IST (Midnight PT)."""
    pt = ZoneInfo('America/Los_Angeles')
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_pt = now_utc.astimezone(pt)
    
    # Next midnight PT
    next_reset_pt = (now_pt + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    now_ist = now_utc.astimezone(ZoneInfo('Asia/Kolkata'))
    next_reset_ist = next_reset_pt.astimezone(ZoneInfo('Asia/Kolkata'))
    
    time_diff = next_reset_ist - now_ist
    
    return {
        "current_ist": now_ist.strftime("%Y-%m-%d %I:%M:%S %p"),
        "reset_ist": next_reset_ist.strftime("%Y-%m-%d %I:%M:%S %p"),
        "time_remaining": str(time_diff).split('.')[0]
    }

def check_ai_studio_key(api_key):
    """Checks validity and quota for an AI Studio key."""
    print(f"--- Checking AI Studio Key ---")
    try:
        genai.configure(api_key=api_key)
        
        # Try a few common models
        models = ['gemini-1.5-flash', 'gemini-1.5-pro']
        success = False
        for model_name in models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test request
                response = model.generate_content("ping", generation_config={"max_output_tokens": 1})
                print(f"✅ Key is VALID (AI Studio) - Verified with {model_name}")
                success = True
                break
            except exceptions.ResourceExhausted:
                print(f"❌ Key is VALID but QUOTA EXHAUSTED for {model_name} (429)")
                success = True
                break
            except exceptions.NotFound:
                continue
            except Exception as e:
                print(f"⚠️ Error with {model_name}: {e}")
                continue
        
        if not success:
            print("❌ Key might be INVALID or has no access to standard models.")
        
    except exceptions.InvalidArgument as e:
        print("❌ Key is INVALID (400 Invalid Argument / API Key)")
        print(f"Details: {e}")
    except Exception as e:
        print(f"❌ Error checking key: {type(e).__name__}: {e}")

def check_vertex_ai():
    """Provides information on checking Vertex AI (Google Cloud) quota."""
    print(f"--- Vertex AI (Google Cloud) ---")
    print("Vertex AI does not use a single 'API Key' like AI Studio. It uses Google Cloud authentication (ADC or Service Account).")
    print("To check Vertex AI quota:")
    print("1. Ensure you are authenticated: `gcloud auth application-default login`")
    print("2. Check Quotas in Cloud Console: https://console.cloud.google.com/iam-admin/quotas")
    print("3. Or use gcloud CLI: `gcloud alpha quotas list --service=aiplatform.googleapis.com` (requires alpha component)")

def main():
    parser = argparse.ArgumentParser(description="Check Gemini API key validity and quota reset time.")
    parser.add_argument("--key", "-k", help="The Gemini API key to check.")
    args = parser.parse_args()

    api_key = args.key
    
    if not api_key:
        try:
            # Check if stdin is a TTY to avoid hanging in non-interactive environments
            if sys.stdin.isatty():
                api_key = input("Please enter the Gemini API key to check: ").strip()
            else:
                print("Error: No API key provided via --key and session is non-interactive.")
                sys.exit(1)
        except EOFError:
            print("\nError: No API key provided.")
            sys.exit(1)

    if not api_key:
        print("Error: No API key provided.")
        sys.exit(1)

    print(f"\nTesting Key: {api_key[:6]}...{api_key[-4:]}")
    
    # Key Type Detection (Heuristic)
    if api_key.startswith("AIza"):
        check_ai_studio_key(api_key)
    else:
        print("⚠️ Key does not match AI Studio format (AIza...). Attempting generic check.")
        check_ai_studio_key(api_key)
        print("\nNote: This might be a Vertex AI key if AI Studio check fails.")
        check_vertex_ai()

    print("\n--- Quota Reallocation Info ---")
    info = calculate_reset_info()
    print(f"Current Time (IST):      {info['current_ist']}")
    print(f"Next Reset (IST):        {info['reset_ist']} (Midnight PT)")
    print(f"Time Until Reallocation: {info['time_remaining']}")

if __name__ == "__main__":
    main()
