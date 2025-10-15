#!/usr/bin/env python3
"""
Simplified MLOps Learning Platform
This version works without external dependencies for demonstration
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Simple in-memory database
users_db = {}
progress_db = {}
current_user = None

# Sample learning content
MODULES = {
    1: {
        "id": 1,
        "title": "MLOps Fundamentals",
        "level": "beginner",
        "content": """
        <h2>What is MLOps?</h2>
        <p>MLOps (Machine Learning Operations) is a set of practices that combines Machine Learning and DevOps to deploy and maintain ML systems in production reliably and efficiently.</p>
        
        <h3>Why MLOps Matters</h3>
        <ul>
            <li>Faster model deployment</li>
            <li>Better model monitoring</li>
            <li>Improved collaboration</li>
            <li>Reduced technical debt</li>
        </ul>
        
        <h3>MLOps Lifecycle</h3>
        <ol>
            <li>Data Management</li>
            <li>Model Development</li>
            <li>Deployment</li>
            <li>Monitoring</li>
            <li>Retraining</li>
        </ol>
        """,
        "summary": "MLOps bridges the gap between ML research and production deployment.",
        "external_resources": [
            {"title": "MLOps Explained", "url": "https://www.youtube.com/watch?v=9_BnHvm-5IY", "type": "video"},
            {"title": "MLOps Best Practices", "url": "https://ml-ops.org/", "type": "article"}
        ]
    },
    2: {
        "id": 2,
        "title": "ML Pipeline Basics",
        "level": "beginner",
        "content": """
        <h2>ML Pipeline Components</h2>
        <p>A typical ML pipeline consists of several interconnected stages:</p>
        
        <h3>1. Data Ingestion</h3>
        <p>Raw data from various sources is collected and stored.</p>
        
        <h3>2. Data Preprocessing</h3>
        <p>Data cleaning, transformation, and feature engineering.</p>
        
        <h3>3. Model Training</h3>
        <p>Using algorithms to learn patterns from the data.</p>
        
        <h3>4. Model Deployment</h3>
        <p>Making the trained model available for predictions.</p>
        """,
        "summary": "ML pipelines automate the end-to-end process from raw data to deployed models.",
        "external_resources": [
            {"title": "ML Pipeline Design", "url": "https://www.kubeflow.org/docs/pipelines/", "type": "documentation"}
        ]
    }
}

class MLOpsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_user
        
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_homepage().encode())
            
        elif self.path == '/dashboard':
            if current_user:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.get_dashboard().encode())
            else:
                self.redirect('/login')
                
        elif self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_login_page().encode())
            
        elif self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_register_page().encode())
            
        elif self.path.startswith('/learn/'):
            if current_user:
                module_id = int(self.path.split('/')[-1])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.get_learning_page(module_id).encode())
            else:
                self.redirect('/login')
                
        elif self.path == '/logout':
            current_user = None
            self.redirect('/')
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1>')
    
    def do_POST(self):
        global current_user
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = urllib.parse.parse_qs(post_data.decode())
        
        if self.path == '/login':
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            
            if username in users_db and users_db[username]['password'] == password:
                current_user = username
                self.redirect('/dashboard')
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.get_login_page(error="Invalid credentials").encode())
                
        elif self.path == '/register':
            username = params.get('username', [''])[0]
            email = params.get('email', [''])[0]
            password = params.get('password', [''])[0]
            
            if username and email and password:
                users_db[username] = {
                    'email': email,
                    'password': password,
                    'created_at': datetime.now().isoformat(),
                    'level': 'beginner',
                    'points': 0
                }
                progress_db[username] = {'completed_modules': [], 'current_module': 1}
                current_user = username
                self.redirect('/dashboard')
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.get_register_page(error="Please fill all fields").encode())
    
    def redirect(self, path):
        self.send_response(302)
        self.send_header('Location', path)
        self.end_headers()
    
    def get_homepage(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MLOps Learning Platform</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }
                .container { max-width: 1200px; margin: 0 auto; }
                .hero { text-align: center; padding: 100px 0; }
                .hero h1 { font-size: 3em; margin-bottom: 20px; }
                .hero p { font-size: 1.2em; margin-bottom: 30px; }
                .btn { background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; font-size: 1.1em; }
                .btn:hover { background: #ff5252; }
                .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 50px 0; }
                .feature { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 10px; text-align: center; }
                .feature h3 { color: #ff6b6b; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>MLOps Learning Platform</h1>
                    <p>Master Machine Learning Operations from Beginner to Expert Level</p>
                    <a href="/register" class="btn">Start Learning</a>
                    <a href="/login" class="btn">Login</a>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <h3>Progressive Learning</h3>
                        <p>Structured curriculum from basics to advanced concepts</p>
                    </div>
                    <div class="feature">
                        <h3>Hands-on Projects</h3>
                        <p>Real-world projects and coding exercises</p>
                    </div>
                    <div class="feature">
                        <h3>Achievement System</h3>
                        <p>Earn badges and track your progress</p>
                    </div>
                    <div class="feature">
                        <h3>External Resources</h3>
                        <p>Curated links to videos, articles, and documentation</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def get_login_page(self, error=None):
        error_msg = f'<div style="color: red; margin: 10px 0;">{error}</div>' if error else ''
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login - MLOps Learning</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
                .login-form {{ background: rgba(255,255,255,0.1); padding: 40px; border-radius: 10px; width: 400px; }}
                .form-group {{ margin: 20px 0; }}
                input {{ width: 100%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; }}
                .btn {{ background: #ff6b6b; color: white; padding: 15px; border: none; border-radius: 5px; width: 100%; font-size: 16px; cursor: pointer; }}
                .btn:hover {{ background: #ff5252; }}
                .links {{ text-align: center; margin-top: 20px; }}
                .links a {{ color: white; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="login-form">
                <h2 style="text-align: center;">Login to MLOps Learning</h2>
                {error_msg}
                <form method="POST" action="/login">
                    <div class="form-group">
                        <input type="text" name="username" placeholder="Username" required>
                    </div>
                    <div class="form-group">
                        <input type="password" name="password" placeholder="Password" required>
                    </div>
                    <button type="submit" class="btn">Login</button>
                </form>
                <div class="links">
                    <a href="/register">Don't have an account? Register here</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    def get_register_page(self, error=None):
        error_msg = f'<div style="color: red; margin: 10px 0;">{error}</div>' if error else ''
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Register - MLOps Learning</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
                .register-form {{ background: rgba(255,255,255,0.1); padding: 40px; border-radius: 10px; width: 400px; }}
                .form-group {{ margin: 20px 0; }}
                input {{ width: 100%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; }}
                .btn {{ background: #ff6b6b; color: white; padding: 15px; border: none; border-radius: 5px; width: 100%; font-size: 16px; cursor: pointer; }}
                .btn:hover {{ background: #ff5252; }}
                .links {{ text-align: center; margin-top: 20px; }}
                .links a {{ color: white; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="register-form">
                <h2 style="text-align: center;">Join MLOps Learning</h2>
                {error_msg}
                <form method="POST" action="/register">
                    <div class="form-group">
                        <input type="text" name="username" placeholder="Username" required>
                    </div>
                    <div class="form-group">
                        <input type="email" name="email" placeholder="Email" required>
                    </div>
                    <div class="form-group">
                        <input type="password" name="password" placeholder="Password" required>
                    </div>
                    <button type="submit" class="btn">Create Account</button>
                </form>
                <div class="links">
                    <a href="/login">Already have an account? Login here</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    def get_dashboard(self):
        user_data = users_db.get(current_user, {})
        progress = progress_db.get(current_user, {'completed_modules': [], 'current_module': 1})
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard - MLOps Learning</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
                .nav {{ margin-bottom: 30px; }}
                .nav a {{ color: white; text-decoration: none; margin-right: 20px; background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 5px; }}
                .modules {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
                .module {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }}
                .module h3 {{ color: #ff6b6b; }}
                .btn {{ background: #ff6b6b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
                .btn:hover {{ background: #ff5252; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .stat {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome back, {current_user}!</h1>
                    <p>Continue your MLOps learning journey</p>
                    <div class="nav">
                        <a href="/dashboard">Dashboard</a>
                        <a href="/logout">Logout</a>
                    </div>
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <h3>{user_data.get('points', 0)}</h3>
                        <p>Total Points</p>
                    </div>
                    <div class="stat">
                        <h3>{len(progress['completed_modules'])}</h3>
                        <p>Modules Completed</p>
                    </div>
                    <div class="stat">
                        <h3>{user_data.get('level', 'Beginner').title()}</h3>
                        <p>Current Level</p>
                    </div>
                </div>
                
                <h2>Learning Modules</h2>
                <div class="modules">
        """
        
        # Debug: Show total modules count
        total_modules = len(MODULES)
        dashboard_html += f"<p><strong>Total Modules Available: {total_modules}</strong></p>"
        
        for module_id, module in MODULES.items():
            completed = module_id in progress['completed_modules']
            status = "Completed" if completed else "Available"
            button_text = "Review" if completed else "Start Learning"
            
            dashboard_html += f"""
                    <div class="module">
                        <h3>{module['title']}</h3>
                        <p><strong>Level:</strong> {module['level'].title()}</p>
                        <p><strong>Status:</strong> {status}</p>
                        <p><strong>Description:</strong> {module['description']}</p>
                        <a href="/learn/{module_id}" class="btn">{button_text}</a>
                    </div>
            """
        
        dashboard_html += """
                </div>
            </div>
        </body>
        </html>
        """
        
        return dashboard_html
    
    def get_learning_page(self, module_id):
        module = MODULES.get(module_id, {})
        if not module:
            return "<h1>Module not found</h1>"
        
        progress = progress_db.get(current_user, {'completed_modules': [], 'current_module': 1})
        completed = module_id in progress['completed_modules']
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{module['title']} - MLOps Learning</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }}
                .container {{ max-width: 1000px; margin: 0 auto; }}
                .header {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
                .nav {{ margin-bottom: 20px; }}
                .nav a {{ color: white; text-decoration: none; margin-right: 20px; background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 5px; }}
                .content {{ background: rgba(255,255,255,0.1); padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
                .resources {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .btn {{ background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
                .btn:hover {{ background: #ff5252; }}
                .resource-link {{ color: #ff6b6b; text-decoration: none; }}
                .resource-link:hover {{ text-decoration: underline; }}
                h2 {{ color: #ff6b6b; }}
                h3 {{ color: #ffd93d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{module['title']}</h1>
                    <p><strong>Level:</strong> {module['level'].title()}</p>
                    <div class="nav">
                        <a href="/dashboard">← Back to Dashboard</a>
                        <a href="/logout">Logout</a>
                    </div>
                </div>
                
                <div class="content">
                    {module['content']}
                </div>
                
                <div class="content">
                    <h2>Summary</h2>
                    <p>{module['summary']}</p>
                </div>
                
                <div class="resources">
                    <h2>External Resources</h2>
                    {"".join([f'<p><a href="{resource["url"]}" target="_blank" class="resource-link">{resource["title"]}</a> ({resource["type"].title()})</p>' for resource in module['external_resources']])}
                </div>
                
                {f'<a href="/dashboard" class="btn">Module Completed - Return to Dashboard</a>' if completed else f'<button onclick="completeModule({module_id})" class="btn">Complete Module</button>'}
            </div>
            
            <script>
                function completeModule(moduleId) {{
                    if (confirm('Mark this module as completed?')) {{
                        // In a real app, this would make an API call
                        alert('Module completed!');
                        window.location.href = '/dashboard';
                    }}
                }}
            </script>
        </body>
        </html>
        """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), MLOpsHandler)
    print(f"MLOps Learning Platform running on http://localhost:{port}")
    print("Features:")
    print("   - User registration and login")
    print("   - Learning modules with content")
    print("   - Progress tracking")
    print("   - External resources")
    print("   - Responsive design")
    print("\nTo access the app, open your browser and go to:")
    print(f"   http://localhost:{port}")
    print("\nDemo users you can create:")
    print("   Username: student1, Email: student1@example.com")
    print("   Username: mlops_user, Email: user@mlops.com")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. Thanks for using MLOps Learning Platform!")
        server.shutdown()
