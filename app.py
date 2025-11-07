import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import logging
from datetime import datetime
from typing import List, Dict, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage
contact_submissions: List[Dict] = []
websocket_clients: Set[tornado.websocket.WebSocketHandler] = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tornado Web App</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                nav {
                    background: #2c3e50;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }
                nav a {
                    color: white;
                    text-decoration: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    transition: all 0.3s ease;
                    background: rgba(255,255,255,0.1);
                }
                nav a:hover {
                    background: rgba(255,255,255,0.2);
                    transform: translateY(-2px);
                }
                .hero {
                    padding: 60px 40px;
                    text-align: center;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .hero h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                    font-weight: 300;
                }
                .hero p {
                    font-size: 1.2em;
                    opacity: 0.9;
                    max-width: 600px;
                    margin: 0 auto 30px;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 30px;
                    padding: 50px 40px;
                    background: white;
                }
                .feature-card {
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    transition: transform 0.3s ease;
                    border: 1px solid #e9ecef;
                }
                .feature-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                }
                .feature-card h3 {
                    color: #2c3e50;
                    margin-bottom: 15px;
                    font-size: 1.4em;
                }
                .feature-card p {
                    color: #6c757d;
                    line-height: 1.6;
                }
                .stats {
                    background: #2c3e50;
                    color: white;
                    padding: 40px;
                    display: flex;
                    justify-content: space-around;
                    flex-wrap: wrap;
                    gap: 20px;
                }
                .stat-item {
                    text-align: center;
                }
                .stat-number {
                    font-size: 2.5em;
                    font-weight: bold;
                    display: block;
                }
                .stat-label {
                    opacity: 0.8;
                    font-size: 0.9em;
                }
                .btn {
                    display: inline-block;
                    background: #3498db;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    border: none;
                    cursor: pointer;
                    font-size: 1em;
                }
                .btn:hover {
                    background: #2980b9;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
                @media (max-width: 768px) {
                    .hero h1 { font-size: 2em; }
                    nav { flex-direction: column; align-items: center; }
                    nav a { width: 200px; text-align: center; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <nav>
                    <a href="/">🏠 Home</a>
                    <a href="/contact">📞 Contact</a>
                    <a href="/chat">💬 Live Chat</a>
                    <a href="/api/health">🔧 API Health</a>
                    <a href="/submissions">📊 Submissions</a>
                </nav>
                
                <div class="hero">
                    <h1>🚀 Tornado Web App</h1>
                    <p>A fully functional web application built with Python Tornado featuring real-time chat, contact forms, and RESTful APIs.</p>
                    <a href="/chat" class="btn">Start Chatting</a>
                </div>
                
                <div class="features">
                    <div class="feature-card">
                        <h3>💬 Real-time Chat</h3>
                        <p>Experience seamless real-time communication with WebSocket technology. Chat with multiple users simultaneously.</p>
                    </div>
                    <div class="feature-card">
                        <h3>📝 Contact Forms</h3>
                        <p>Beautiful and functional contact forms with validation and in-memory storage. Perfect for user feedback.</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔧 REST API</h3>
                        <p>Health check endpoints and JSON APIs. Monitor your application status and integrate with other services.</p>
                    </div>
                    <div class="feature-card">
                        <h3>⚡ High Performance</h3>
                        <p>Built on Tornado's asynchronous networking library for high performance and scalability.</p>
                    </div>
                </div>
                
                <div class="stats">
                    <div class="stat-item">
                        <span class="stat-number" id="chatUsers">0</span>
                        <span class="stat-label">Active Chat Users</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="submissionsCount">0</span>
                        <span class="stat-label">Contact Submissions</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">100%</span>
                        <span class="stat-label">Uptime</span>
                    </div>
                </div>
            </div>

            <script>
                // Update stats dynamically
                async function updateStats() {
                    try {
                        const response = await fetch('/api/health');
                        const data = await response.json();
                        document.getElementById('chatUsers').textContent = data.websocket_clients_count;
                        document.getElementById('submissionsCount').textContent = data.contact_submissions_count;
                    } catch (error) {
                        console.log('Stats update failed:', error);
                    }
                }
                
                // Update stats every 10 seconds
                updateStats();
                setInterval(updateStats, 10000);
            </script>
        </body>
        </html>
        """
        self.write(html)

class ContactHandler(tornado.web.RequestHandler):
    def get(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contact Us - Tornado Web App</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                nav {
                    background: #2c3e50;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }
                nav a {
                    color: white;
                    text-decoration: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    transition: all 0.3s ease;
                    background: rgba(255,255,255,0.1);
                }
                nav a:hover {
                    background: rgba(255,255,255,0.2);
                    transform: translateY(-2px);
                }
                .content {
                    padding: 50px;
                }
                h1 {
                    color: #2c3e50;
                    text-align: center;
                    margin-bottom: 40px;
                    font-size: 2.5em;
                    font-weight: 300;
                }
                .form-group {
                    margin-bottom: 25px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: 600;
                    color: #2c3e50;
                }
                input, textarea {
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: border-color 0.3s ease;
                }
                input:focus, textarea:focus {
                    outline: none;
                    border-color: #3498db;
                }
                textarea {
                    resize: vertical;
                    min-height: 120px;
                }
                .btn {
                    background: #3498db;
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: block;
                    width: 200px;
                    margin: 30px auto 0;
                }
                .btn:hover {
                    background: #2980b9;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }
                .success-message {
                    background: #d4edda;
                    color: #155724;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 30px;
                    border: 1px solid #c3e6cb;
                }
                @media (max-width: 768px) {
                    .content { padding: 30px 20px; }
                    nav { flex-direction: column; align-items: center; }
                    nav a { width: 200px; text-align: center; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <nav>
                    <a href="/">🏠 Home</a>
                    <a href="/contact">📞 Contact</a>
                    <a href="/chat">💬 Live Chat</a>
                    <a href="/api/health">🔧 API Health</a>
                    <a href="/submissions">📊 Submissions</a>
                </nav>
                
                <div class="content">
                    <h1>📞 Contact Us</h1>
                    <form method="POST">
                        <div class="form-group">
                            <label for="name">Full Name:</label>
                            <input type="text" id="name" name="name" required placeholder="Enter your full name">
                        </div>
                        <div class="form-group">
                            <label for="email">Email Address:</label>
                            <input type="email" id="email" name="email" required placeholder="Enter your email address">
                        </div>
                        <div class="form-group">
                            <label for="message">Your Message:</label>
                            <textarea id="message" name="message" required placeholder="Tell us what's on your mind..."></textarea>
                        </div>
                        <button type="submit" class="btn">Send Message</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.write(html)
    
    def post(self):
        try:
            name = self.get_body_argument("name", "").strip()
            email = self.get_body_argument("email", "").strip()
            message = self.get_body_argument("message", "").strip()
            
            if not all([name, email, message]):
                self.set_status(400)
                self.write("All fields are required")
                return
            
            submission = {
                "id": len(contact_submissions) + 1,
                "name": name,
                "email": email,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "ip": self.request.remote_ip
            }
            contact_submissions.append(submission)
            logger.info(f"New contact submission from {name} ({email})")
            
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Thank You - Tornado Web App</title>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    nav {{
                        background: #2c3e50;
                        padding: 20px;
                        display: flex;
                        justify-content: center;
                        flex-wrap: wrap;
                        gap: 15px;
                    }}
                    nav a {{
                        color: white;
                        text-decoration: none;
                        padding: 12px 24px;
                        border-radius: 25px;
                        transition: all 0.3s ease;
                        background: rgba(255,255,255,0.1);
                    }}
                    nav a:hover {{
                        background: rgba(255,255,255,0.2);
                        transform: translateY(-2px);
                    }}
                    .content {{
                        padding: 50px;
                        text-align: center;
                    }}
                    .success-message {{
                        background: #d4edda;
                        color: #155724;
                        padding: 30px;
                        border-radius: 10px;
                        margin-bottom: 30px;
                        border: 1px solid #c3e6cb;
                    }}
                    h1 {{
                        color: #27ae60;
                        margin-bottom: 20px;
                    }}
                    p {{
                        color: #6c757d;
                        margin-bottom: 15px;
                        line-height: 1.6;
                    }}
                    .btn {{
                        display: inline-block;
                        background: #3498db;
                        color: white;
                        padding: 12px 30px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: bold;
                        transition: all 0.3s ease;
                        margin: 10px;
                    }}
                    .btn:hover {{
                        background: #2980b9;
                        transform: translateY(-2px);
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <nav>
                        <a href="/">🏠 Home</a>
                        <a href="/contact">📞 Contact</a>
                        <a href="/chat">💬 Live Chat</a>
                        <a href="/api/health">🔧 API Health</a>
                        <a href="/submissions">📊 Submissions</a>
                    </nav>
                    
                    <div class="content">
                        <div class="success-message">
                            <h1>✅ Thank You, {name}!</h1>
                            <p>Your message has been successfully received.</p>
                            <p>We'll get back to you at <strong>{email}</strong> within 24 hours.</p>
                        </div>
                        <a href="/contact" class="btn">Send Another Message</a>
                        <a href="/" class="btn">Return to Home</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.write(html)
        except Exception as e:
            logger.error(f"Error processing contact form: {e}")
            self.set_status(500)
            self.write("An error occurred while processing your submission")

class SubmissionsHandler(tornado.web.RequestHandler):
    def get(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Submissions - Tornado Web App</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                nav {
                    background: #2c3e50;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }
                nav a {
                    color: white;
                    text-decoration: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    transition: all 0.3s ease;
                    background: rgba(255,255,255,0.1);
                }
                nav a:hover {
                    background: rgba(255,255,255,0.2);
                    transform: translateY(-2px);
                }
                .content {
                    padding: 40px;
                }
                h1 {
                    color: #2c3e50;
                    text-align: center;
                    margin-bottom: 30px;
                    font-size: 2.5em;
                }
                .submissions-list {
                    display: grid;
                    gap: 20px;
                }
                .submission-card {
                    background: #f8f9fa;
                    padding: 25px;
                    border-radius: 10px;
                    border-left: 5px solid #3498db;
                }
                .submission-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    flex-wrap: wrap;
                    gap: 10px;
                }
                .submission-name {
                    font-weight: bold;
                    color: #2c3e50;
                    font-size: 1.2em;
                }
                .submission-email {
                    color: #3498db;
                }
                .submission-time {
                    color: #6c757d;
                    font-size: 0.9em;
                }
                .submission-message {
                    color: #495057;
                    line-height: 1.6;
                    background: white;
                    padding: 15px;
                    border-radius: 5px;
                    border: 1px solid #e9ecef;
                }
                .empty-state {
                    text-align: center;
                    padding: 60px 20px;
                    color: #6c757d;
                }
                .empty-state h2 {
                    margin-bottom: 15px;
                    font-weight: 300;
                }
                .btn {
                    display: inline-block;
                    background: #3498db;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    border: none;
                    cursor: pointer;
                    margin-top: 20px;
                }
                .btn:hover {
                    background: #2980b9;
                    transform: translateY(-2px);
                }
                @media (max-width: 768px) {
                    .content { padding: 20px; }
                    nav { flex-direction: column; align-items: center; }
                    nav a { width: 200px; text-align: center; }
                    .submission-header { flex-direction: column; align-items: flex-start; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <nav>
                    <a href="/">🏠 Home</a>
                    <a href="/contact">📞 Contact</a>
                    <a href="/chat">💬 Live Chat</a>
                    <a href="/api/health">🔧 API Health</a>
                    <a href="/submissions">📊 Submissions</a>
                </nav>
                
                <div class="content">
                    <h1>📊 Contact Submissions</h1>
                    <div class="submissions-list" id="submissionsList">
                        <!-- Submissions will be loaded here -->
                    </div>
                </div>
            </div>

            <script>
                function escapeHtml(unsafe) {
                    return unsafe
                        .replace(/&/g, "&amp;")
                        .replace(/</g, "&lt;")
                        .replace(/>/g, "&gt;")
                        .replace(/"/g, "&quot;")
                        .replace(/'/g, "&#039;");
                }
                
                async function loadSubmissions() {
                    try {
                        const response = await fetch('/api/submissions');
                        const submissions = await response.json();
                        
                        const container = document.getElementById('submissionsList');
                        
                        if (submissions.length === 0) {
                            container.innerHTML = `
                                <div class="empty-state">
                                    <h2>No submissions yet</h2>
                                    <p>Be the first to send us a message!</p>
                                    <a href="/contact" class="btn">Send a Message</a>
                                </div>
                            `;
                            return;
                        }
                        
                        container.innerHTML = submissions.map(sub => `
                            <div class="submission-card">
                                <div class="submission-header">
                                    <span class="submission-name">${escapeHtml(sub.name)}</span>
                                    <span class="submission-email">${escapeHtml(sub.email)}</span>
                                    <span class="submission-time">${new Date(sub.timestamp).toLocaleString()}</span>
                                </div>
                                <div class="submission-message">${escapeHtml(sub.message)}</div>
                            </div>
                        `).join('');
                    } catch (error) {
                        console.error('Error loading submissions:', error);
                        document.getElementById('submissionsList').innerHTML = '<p>Error loading submissions</p>';
                    }
                }
                
                loadSubmissions();
            </script>
        </body>
        </html>
        """
        self.write(html)

class ChatHandler(tornado.web.RequestHandler):
    def get(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Live Chat - Tornado Web App</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                    height: 80vh;
                    display: flex;
                    flex-direction: column;
                }
                nav {
                    background: #2c3e50;
                    padding: 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }
                .nav-links {
                    display: flex;
                    gap: 15px;
                    flex-wrap: wrap;
                }
                nav a {
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 20px;
                    transition: all 0.3s ease;
                    background: rgba(255,255,255,0.1);
                }
                nav a:hover {
                    background: rgba(255,255,255,0.2);
                    transform: translateY(-2px);
                }
                .chat-info {
                    color: white;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }
                .user-count {
                    background: rgba(255,255,255,0.2);
                    padding: 5px 15px;
                    border-radius: 15px;
                    font-size: 0.9em;
                }
                .chat-container {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    padding: 0;
                }
                .chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 20px;
                    background: #f8f9fa;
                }
                .message {
                    margin-bottom: 15px;
                    display: flex;
                    flex-direction: column;
                }
                .message.own {
                    align-items: flex-end;
                }
                .message.other {
                    align-items: flex-start;
                }
                .message-bubble {
                    max-width: 70%;
                    padding: 12px 18px;
                    border-radius: 18px;
                    position: relative;
                    word-wrap: break-word;
                }
                .message.own .message-bubble {
                    background: #3498db;
                    color: white;
                    border-bottom-right-radius: 5px;
                }
                .message.other .message-bubble {
                    background: white;
                    color: #333;
                    border: 1px solid #e9ecef;
                    border-bottom-left-radius: 5px;
                }
                .message-sender {
                    font-size: 0.8em;
                    color: #6c757d;
                    margin-bottom: 5px;
                    padding: 0 10px;
                }
                .message-time {
                    font-size: 0.7em;
                    opacity: 0.7;
                    margin-top: 5px;
                    text-align: right;
                }
                .system-message {
                    text-align: center;
                    color: #6c757d;
                    font-style: italic;
                    margin: 10px 0;
                    font-size: 0.9em;
                }
                .chat-input-container {
                    padding: 20px;
                    background: white;
                    border-top: 1px solid #e9ecef;
                    display: flex;
                    gap: 10px;
                }
                #messageInput {
                    flex: 1;
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 25px;
                    font-size: 16px;
                    outline: none;
                    transition: border-color 0.3s ease;
                }
                #messageInput:focus {
                    border-color: #3498db;
                }
                #sendButton {
                    background: #3498db;
                    color: white;
                    border: none;
                    padding: 15px 25px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: all 0.3s ease;
                }
                #sendButton:hover:not(:disabled) {
                    background: #2980b9;
                    transform: translateY(-2px);
                }
                #sendButton:disabled {
                    background: #bdc3c7;
                    cursor: not-allowed;
                }
                .connection-status {
                    padding: 10px 20px;
                    text-align: center;
                    font-size: 0.9em;
                    background: #fff3cd;
                    color: #856404;
                    border-bottom: 1px solid #ffeaa7;
                }
                .connection-status.connected {
                    background: #d1ecf1;
                    color: #0c5460;
                }
                @media (max-width: 768px) {
                    .container { height: 90vh; margin: 10px; }
                    nav { flex-direction: column; }
                    .nav-links { justify-content: center; }
                    .message-bubble { max-width: 85%; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <nav>
                    <div class="nav-links">
                        <a href="/">🏠 Home</a>
                        <a href="/contact">📞 Contact</a>
                        <a href="/chat">💬 Live Chat</a>
                        <a href="/api/health">🔧 API Health</a>
                        <a href="/submissions">📊 Submissions</a>
                    </div>
                    <div class="chat-info">
                        <span class="user-count">👥 <span id="userCount">0</span> users online</span>
                    </div>
                </nav>
                
                <div class="connection-status" id="connectionStatus">
                    🔄 Connecting to chat...
                </div>
                
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages"></div>
                    
                    <div class="chat-input-container">
                        <input type="text" id="messageInput" placeholder="Type your message here..." maxlength="500" disabled>
                        <button id="sendButton" disabled>Send</button>
                    </div>
                </div>
            </div>

            <script>
                let ws = null;
                let username = "User_" + Math.floor(Math.random() * 10000);
                let isConnected = false;
                
                function connect() {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    const wsUrl = protocol + '//' + window.location.host + '/websocket';
                    
                    ws = new WebSocket(wsUrl);
                    
                    ws.onopen = function() {
                        console.log('WebSocket connected');
                        isConnected = true;
                        updateConnectionStatus(true);
                        document.getElementById('messageInput').disabled = false;
                        document.getElementById('sendButton').disabled = false;
                        addSystemMessage('Connected to chat room');
                    };
                    
                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        console.log('Received:', data);
                        
                        if (data.type === 'message') {
                            addMessage(data.sender, data.message, data.timestamp, data.sender === username);
                        } else if (data.type === 'user_count') {
                            document.getElementById('userCount').textContent = data.count;
                        } else if (data.type === 'system') {
                            addSystemMessage(data.message);
                        } else if (data.type === 'chat_history') {
                            data.messages.forEach(msg => {
                                addMessage(msg.sender, msg.message, msg.timestamp, msg.sender === username, true);
                            });
                        }
                    };
                    
                    ws.onclose = function() {
                        console.log('WebSocket disconnected');
                        isConnected = false;
                        updateConnectionStatus(false);
                        document.getElementById('messageInput').disabled = true;
                        document.getElementById('sendButton').disabled = true;
                        addSystemMessage('Disconnected from chat room');
                        
                        // Attempt to reconnect after 3 seconds
                        setTimeout(connect, 3000);
                    };
                    
                    ws.onerror = function(error) {
                        console.error('WebSocket error:', error);
                        updateConnectionStatus(false);
                    };
                }
                
                function updateConnectionStatus(connected) {
                    const statusEl = document.getElementById('connectionStatus');
                    if (connected) {
                        statusEl.textContent = '✅ Connected to chat';
                        statusEl.className = 'connection-status connected';
                    } else {
                        statusEl.textContent = '🔴 Disconnected - Attempting to reconnect...';
                        statusEl.className = 'connection-status';
                    }
                }
                
                function sendMessage() {
                    const messageInput = document.getElementById('messageInput');
                    const message = messageInput.value.trim();
                    
                    if (message && ws && ws.readyState === WebSocket.OPEN) {
                        const messageData = {
                            type: 'message',
                            sender: username,
                            message: message,
                            timestamp: new Date().toISOString()
                        };
                        
                        ws.send(JSON.stringify(messageData));
                        messageInput.value = '';
                    }
                }
                
                function addMessage(sender, message, timestamp, isOwn, isHistory = false) {
                    const messagesDiv = document.getElementById('chatMessages');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${isOwn ? 'own' : 'other'}`;
                    
                    const senderEl = document.createElement('div');
                    senderEl.className = 'message-sender';
                    senderEl.textContent = isOwn ? 'You' : sender;
                    
                    const bubbleEl = document.createElement('div');
                    bubbleEl.className = 'message-bubble';
                    bubbleEl.textContent = message;
                    
                    const timeEl = document.createElement('div');
                    timeEl.className = 'message-time';
                    timeEl.textContent = new Date(timestamp).toLocaleTimeString();
                    
                    messageDiv.appendChild(senderEl);
                    messageDiv.appendChild(bubbleEl);
                    messageDiv.appendChild(timeEl);
                    messagesDiv.appendChild(messageDiv);
                    
                    if (!isHistory) {
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    }
                }
                
                function addSystemMessage(message) {
                    const messagesDiv = document.getElementById('chatMessages');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'system-message';
                    messageDiv.textContent = message;
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                // Event listeners
                document.getElementById('sendButton').addEventListener('click', sendMessage);
                document.getElementById('messageInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
                
                // Initialize connection when page loads
                window.addEventListener('load', connect);
            </script>
        </body>
        </html>
        """
        self.write(html)

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Tornado Web Application",
            "version": "1.0.0",
            "contact_submissions_count": len(contact_submissions),
            "websocket_clients_count": len(websocket_clients),
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "uptime": "running"
        }
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(health_data, indent=2))

class SubmissionsAPIHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(contact_submissions, indent=2))

class ChatWebSocket(tornado.websocket.WebSocketHandler):
    # Store chat history
    chat_history = []
    
    def open(self):
        websocket_clients.add(self)
        logger.info(f"WebSocket connection opened. Total clients: {len(websocket_clients)}")
        self.broadcast_user_count()
        self.send_system_message(f"User joined the chat")
        
        # Send chat history to the new client
        if self.chat_history:
            self.write_message(json.dumps({
                'type': 'chat_history',
                'messages': self.chat_history[-50:]  # Last 50 messages
            }))
    
    def on_message(self, message):
        try:
            data = json.loads(message)
            if data.get('type') == 'message':
                message_data = {
                    'type': 'message',
                    'sender': data.get('sender', 'Anonymous'),
                    'message': data.get('message', ''),
                    'timestamp': data.get('timestamp', datetime.now().isoformat())
                }
                
                # Store in history
                self.chat_history.append(message_data)
                # Keep only last 100 messages
                if len(self.chat_history) > 100:
                    self.chat_history = self.chat_history[-100:]
                
                # Broadcast to all clients
                self.broadcast(message_data)
                logger.info(f"Chat message from {message_data['sender']}: {message_data['message'][:50]}...")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {message}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def on_close(self):
        websocket_clients.discard(self)
        logger.info(f"WebSocket connection closed. Total clients: {len(websocket_clients)}")
        self.broadcast_user_count()
        self.send_system_message("User left the chat")
    
    def broadcast(self, message):
        disconnected_clients = set()
        for client in websocket_clients:
            try:
                client.write_message(json.dumps(message))
            except:
                disconnected_clients.add(client)
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            websocket_clients.discard(client)
    
    def broadcast_user_count(self):
        user_count_message = {
            'type': 'user_count',
            'count': len(websocket_clients)
        }
        self.broadcast(user_count_message)
    
    def send_system_message(self, message):
        system_message = {
            'type': 'system',
            'message': message
        }
        self.broadcast(system_message)
    
    def check_origin(self, origin):
        return True

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/contact", ContactHandler),
        (r"/chat", ChatHandler),
        (r"/submissions", SubmissionsHandler),
        (r"/api/health", HealthHandler),
        (r"/api/submissions", SubmissionsAPIHandler),
        (r"/websocket", ChatWebSocket),
    ], autoreload=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app = make_app()
    app.listen(port, address='0.0.0.0')
    logger.info(f"✅ Tornado running on http://0.0.0.0:{port}")
    logger.info(f"✅ Local access: http://localhost:{port}")
    logger.info("🚀 Application started successfully!")
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")