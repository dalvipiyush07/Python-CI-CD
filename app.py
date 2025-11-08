from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LearnHub - Create & Sell Online Courses</title>
    <style>
        :root {
            --primary: #6c63ff;
            --secondary: #4d44db;
            --dark: #2a2a72;
            --light: #f8f9fa;
            --accent: #ff7d00;
            --success: #28a745;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        body {
            background-color: var(--light);
            color: #333;
            line-height: 1.6;
        }
        
        header {
            background: linear-gradient(135deg, var(--dark), var(--secondary));
            color: white;
            padding: 2rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
        }
        
        .logo span {
            color: var(--accent);
        }
        
        nav ul {
            display: flex;
            list-style: none;
        }
        
        nav ul li {
            margin-left: 2rem;
        }
        
        nav ul li a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        nav ul li a:hover {
            color: var(--accent);
        }
        
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        }
        
        .hero {
            padding: 5rem 0;
            text-align: center;
        }
        
        .hero-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            line-height: 1.2;
        }
        
        .hero p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .cta-button {
            display: inline-block;
            background-color: var(--accent);
            color: white;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            margin: 0.5rem;
            border: none;
            cursor: pointer;
        }
        
        .cta-button.outline {
            background-color: transparent;
            border: 2px solid white;
        }
        
        .cta-button:hover {
            background-color: #ff6a00;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .cta-button.outline:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .features {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin: 4rem 0;
            gap: 2rem;
        }
        
        .feature-card {
            flex: 1 1 300px;
            background: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease;
            text-align: center;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 1rem;
            display: inline-block;
        }
        
        .feature-title {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: var(--dark);
        }
        
        .how-it-works {
            background-color: white;
            padding: 4rem 2rem;
            border-radius: 10px;
            margin: 4rem 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }
        
        h2 {
            color: var(--dark);
            margin-bottom: 2rem;
            text-align: center;
            font-size: 2.2rem;
        }
        
        .steps {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .step {
            flex: 1 1 250px;
            text-align: center;
            padding: 1.5rem;
            position: relative;
        }
        
        .step-number {
            background-color: var(--primary);
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-weight: bold;
            font-size: 1.2rem;
        }
        
        .step:not(:last-child):after {
            content: "";
            position: absolute;
            top: 25px;
            right: -30px;
            width: 30px;
            height: 2px;
            background-color: var(--primary);
            opacity: 0.3;
        }
        
        .course-showcase {
            margin: 4rem 0;
        }
        
        .course-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .course-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        
        .course-card:hover {
            transform: translateY(-10px);
        }
        
        .course-image {
            height: 180px;
            background-color: #ddd;
            background-size: cover;
            background-position: center;
        }
        
        .course-content {
            padding: 1.5rem;
        }
        
        .course-category {
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        
        .course-title {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        
        .course-instructor {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 1rem;
        }
        
        .course-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
        }
        
        .course-price {
            font-weight: 700;
            color: var(--dark);
        }
        
        .course-rating {
            color: var(--accent);
            font-weight: 600;
        }
        
        .testimonials {
            margin: 4rem 0;
        }
        
        .testimonial-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .testimonial {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            position: relative;
        }
        
        .testimonial:before {
            content: '"';
            font-size: 5rem;
            color: var(--light);
            position: absolute;
            top: 10px;
            left: 10px;
            line-height: 1;
            z-index: 0;
            opacity: 0.5;
        }
        
        .testimonial-content {
            position: relative;
            z-index: 1;
        }
        
        .testimonial-text {
            font-style: italic;
            margin-bottom: 1rem;
        }
        
        .testimonial-author {
            display: flex;
            align-items: center;
        }
        
        .author-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #ddd;
            margin-right: 1rem;
            background-size: cover;
            background-position: center;
        }
        
        .author-info h4 {
            color: var(--dark);
            margin-bottom: 0.2rem;
        }
        
        .author-info p {
            color: #666;
            font-size: 0.8rem;
        }
        
        .pricing {
            background-color: white;
            padding: 4rem 2rem;
            border-radius: 10px;
            margin: 4rem 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        }
        
        .pricing-plans {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .pricing-card {
            background: white;
            border-radius: 10px;
            padding: 2rem;
            flex: 1 1 300px;
            max-width: 350px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            border: 2px solid #eee;
            transition: all 0.3s ease;
        }
        
        .pricing-card.popular {
            border-color: var(--primary);
            position: relative;
        }
        
        .popular-badge {
            position: absolute;
            top: -12px;
            right: 20px;
            background-color: var(--primary);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .pricing-card.popular .cta-button {
            background-color: var(--primary);
        }
        
        .pricing-card.popular .cta-button:hover {
            background-color: var(--secondary);
        }
        
        .pricing-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }
        
        .pricing-title {
            font-size: 1.5rem;
            color: var(--dark);
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .pricing-amount {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .pricing-amount span {
            font-size: 1rem;
            color: #666;
        }
        
        .pricing-features {
            list-style: none;
            margin-bottom: 2rem;
        }
        
        .pricing-features li {
            margin-bottom: 0.8rem;
            position: relative;
            padding-left: 1.8rem;
        }
        
        .pricing-features li:before {
            content: "✓";
            color: var(--success);
            position: absolute;
            left: 0;
            font-weight: bold;
        }
        
        .pricing-features li.disabled {
            color: #999;
        }
        
        .pricing-features li.disabled:before {
            content: "✗";
            color: #ccc;
        }
        
        .cta-section {
            background: linear-gradient(135deg, var(--dark), var(--secondary));
            color: white;
            padding: 5rem 0;
            text-align: center;
        }
        
        .cta-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .cta-section h2 {
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .cta-section p {
            margin-bottom: 2rem;
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            max-width: 500px;
            width: 90%;
            position: relative;
        }
        
        .close-modal {
            position: absolute;
            top: 15px;
            right: 15px;
            font-size: 1.5rem;
            cursor: pointer;
            background: none;
            border: none;
        }
        
        .modal h3 {
            margin-bottom: 1.5rem;
            color: var(--dark);
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 0.8rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .form-group textarea {
            min-height: 100px;
        }
        
        footer {
            background-color: var(--dark);
            color: white;
            padding: 4rem 0 2rem;
        }
        
        .footer-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 3rem;
        }
        
        .footer-logo {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            display: inline-block;
        }
        
        .footer-logo span {
            color: var(--accent);
        }
        
        .footer-about p {
            margin-bottom: 1.5rem;
            opacity: 0.8;
        }
        
        .social-links {
            display: flex;
            gap: 1rem;
        }
        
        .social-links a {
            color: white;
            font-size: 1.2rem;
            transition: color 0.3s ease;
            text-decoration: none;
        }
        
        .social-links a:hover {
            color: var(--accent);
        }
        
        .footer-links h3 {
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            position: relative;
            padding-bottom: 0.5rem;
        }
        
        .footer-links h3:after {
            content: "";
            position: absolute;
            left: 0;
            bottom: 0;
            width: 40px;
            height: 2px;
            background-color: var(--accent);
        }
        
        .footer-links ul {
            list-style: none;
        }
        
        .footer-links ul li {
            margin-bottom: 0.8rem;
        }
        
        .footer-links ul li a {
            color: white;
            opacity: 0.8;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .footer-links ul li a:hover {
            opacity: 1;
            padding-left: 5px;
        }
        
        .footer-newsletter p {
            opacity: 0.8;
            margin-bottom: 1.5rem;
        }
        
        .newsletter-form {
            display: flex;
            margin-bottom: 1rem;
        }
        
        .newsletter-form input {
            flex: 1;
            padding: 0.8rem;
            border: none;
            border-radius: 4px 0 0 4px;
        }
        
        .newsletter-form button {
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 0 1.2rem;
            border-radius: 0 4px 4px 0;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .newsletter-form button:hover {
            background-color: #ff6a00;
        }
        
        .copyright {
            text-align: center;
            padding-top: 2rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            opacity: 0.7;
            font-size: 0.9rem;
        }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: var(--success);
            color: white;
            padding: 1rem 2rem;
            border-radius: 5px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }
        
        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                text-align: center;
            }
            
            nav {
                width: 100%;
                margin-top: 1.5rem;
                display: none;
            }
            
            nav.active {
                display: block;
            }
            
            nav ul {
                flex-direction: column;
                align-items: center;
            }
            
            nav ul li {
                margin: 0.5rem 0;
            }
            
            .mobile-menu-btn {
                display: block;
                position: absolute;
                top: 25px;
                right: 20px;
            }
            
            h1 {
                font-size: 2.2rem;
            }
            
            .hero p {
                font-size: 1rem;
            }
            
            .step:not(:last-child):after {
                display: none;
            }
            
            .pricing-plans {
                flex-direction: column;
                align-items: center;
            }
            
            .pricing-card {
                width: 100%;
                max-width: 400px;
            }
        }
        
        @media (max-width: 480px) {
            .cta-button {
                display: block;
                margin: 0.5rem auto;
            }
            
            .newsletter-form {
                flex-direction: column;
            }
            
            .newsletter-form input,
            .newsletter-form button {
                border-radius: 4px;
            }
            
            .newsletter-form button {
                padding: 0.8rem;
                margin-top: 0.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-container">
            <a href="#" class="logo">Learn<span>Hub</span></a>
            <button class="mobile-menu-btn">☰</button>
            <nav id="main-nav">
                <ul>
                    <li><a href="#features">Features</a></li>
                    <li><a href="#how-it-works">How It Works</a></li>
                    <li><a href="#courses">Courses</a></li>
                    <li><a href="#pricing">Pricing</a></li>
                    <li><a href="#testimonials">Testimonials</a></li>
                </ul>
            </nav>
        </div>
        
        <div class="hero">
            <div class="hero-content">
                <h1>Create & Sell Your Online Courses</h1>
                <p>Join thousands of instructors earning money by sharing their knowledge. Our platform makes it easy to create, market, and sell your courses to students worldwide.</p>
                <div>
                    <button class="cta-button" id="signup-btn">Start Teaching Today</button>
                    <a href="#courses" class="cta-button outline">Explore Courses</a>
                </div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <section id="features" class="features">
            <div class="feature-card">
                <div class="feature-icon">🎓</div>
                <h3 class="feature-title">Easy Course Creation</h3>
                <p>Our intuitive course builder helps you create professional courses with videos, quizzes, and downloads in minutes.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">💸</div>
                <h3 class="feature-title">Earn Money</h3>
                <p>Keep up to 80% of each sale with our competitive revenue sharing model. Get paid monthly via PayPal or bank transfer.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <h3 class="feature-title">Marketing Tools</h3>
                <p>Built-in marketing features help you promote your courses with coupons, affiliates, and email campaigns.</p>
            </div>
        </section>
        
        <section id="how-it-works" class="how-it-works">
            <h2>How LearnHub Works</h2>
            <p style="text-align: center; max-width: 700px; margin: 0 auto;">Whether you're an expert, educator, or entrepreneur, you can launch your online course in just a few simple steps.</p>
            
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>Sign Up</h3>
                    <p>Create your free instructor account in minutes. No upfront costs or commitments.</p>
                </div>
                
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Create Your Course</h3>
                    <p>Use our tools to build engaging content with videos, presentations, quizzes and more.</p>
                </div>
                
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Publish</h3>
                    <p>Submit your course for review. We'll help optimize it for maximum student engagement.</p>
                </div>
                
                <div class="step">
                    <div class="step-number">4</div>
                    <h3>Earn</h3>
                    <p>Start earning as students enroll in your course. We handle payments and hosting.</p>
                </div>
            </div>
        </section>
        
        <section id="courses" class="course-showcase">
            <h2>Popular Course Categories</h2>
            <p style="text-align: center; margin-bottom: 2rem;">Browse some of our top-performing courses to get inspiration for your own.</p>
            
            <div class="course-grid">
                <div class="course-card" onclick="showCourseModal('The Complete JavaScript Course 2024')">
                    <div class="course-image" style="background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60');"></div>
                    <div class="course-content">
                        <div class="course-category">Web Development</div>
                        <h3 class="course-title">The Complete JavaScript Course 2024</h3>
                        <div class="course-instructor">By John Smith</div>
                        <div class="course-meta">
                            <div class="course-price">$89.99</div>
                            <div class="course-rating">★ 4.8 (1,245)</div>
                        </div>
                    </div>
                </div>
                
                <div class="course-card" onclick="showCourseModal('Python for Data Analysis')">
                    <div class="course-image" style="background-image: url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60');"></div>
                    <div class="course-content">
                        <div class="course-category">Data Science</div>
                        <h3 class="course-title">Python for Data Analysis</h3>
                        <div class="course-instructor">By Sarah Johnson</div>
                        <div class="course-meta">
                            <div class="course-price">$79.99</div>
                            <div class="course-rating">★ 4.7 (892)</div>
                        </div>
                    </div>
                </div>
                
                <div class="course-card" onclick="showCourseModal('Digital Photography Masterclass')">
                    <div class="course-image" style="background-image: url('https://images.unsplash.com/photo-1579389083078-4e7018379f7e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60');"></div>
                    <div class="course-content">
                        <div class="course-category">Photography</div>
                        <h3 class="course-title">Digital Photography Masterclass</h3>
                        <div class="course-instructor">By Michael Brown</div>
                        <div class="course-meta">
                            <div class="course-price">$69.99</div>
                            <div class="course-rating">★ 4.9 (2,103)</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="testimonials" class="testimonials">
            <h2>What Our Instructors Say</h2>
            <p style="text-align: center; margin-bottom: 2rem;">Hear from instructors who've built successful businesses on LearnHub.</p>
            
            <div class="testimonial-grid">
                <div class="testimonial">
                    <div class="testimonial-content">
                        <p class="testimonial-text">LearnHub has allowed me to turn my expertise into a full-time income. In my first year, I earned over $75,000 from my photography courses.</p>
                        <div class="testimonial-author">
                            <div class="author-avatar" style="background-image: url('https://randomuser.me/api/portraits/women/32.jpg');"></div>
                            <div class="author-info">
                                <h4>Jessica Wilson</h4>
                                <p>Photography Instructor</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="testimonial">
                    <div class="testimonial-content">
                        <p class="testimonial-text">The platform is incredibly easy to use. I was able to create and launch my first course in just two weeks, and now it's my primary source of income.</p>
                        <div class="testimonial-author">
                            <div class="author-avatar" style="background-image: url('https://randomuser.me/api/portraits/men/45.jpg');"></div>
                            <div class="author-info">
                                <h4>David Chen</h4>
                                <p>Programming Instructor</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="testimonial">
                    <div class="testimonial-content">
                        <p class="testimonial-text">What I love most is the community. The support team and other instructors are always willing to help and share strategies for success.</p>
                        <div class="testimonial-author">
                            <div class="author-avatar" style="background-image: url('https://randomuser.me/api/portraits/women/68.jpg');"></div>
                            <div class="author-info">
                                <h4>Maria Garcia</h4>
                                <p>Business Instructor</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="pricing" class="pricing">
            <h2>Simple, Transparent Pricing</h2>
            <p style="text-align: center; margin-bottom: 2rem;">Choose the plan that works best for you. No hidden fees, cancel anytime.</p>
            
            <div class="pricing-plans">
                <div class="pricing-card">
                    <h3 class="pricing-title">Starter</h3>
                    <div class="pricing-amount">$0<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>5% transaction fee</li>
                        <li>Basic course analytics</li>
                        <li>Email support</li>
                        <li class="disabled">Marketing tools</li>
                        <li class="disabled">Affiliate program</li>
                        <li class="disabled">Custom domain</li>
                    </ul>
                    <button class="cta-button outline" onclick="selectPlan('Starter')">Get Started</button>
                </div>
                
                <div class="pricing-card popular">
                    <div class="popular-badge">Most Popular</div>
                    <h3 class="pricing-title">Professional</h3>
                    <div class="pricing-amount">$29<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>3% transaction fee</li>
                        <li>Advanced analytics</li>
                        <li>Priority support</li>
                        <li>Basic marketing tools</li>
                        <li>Affiliate program</li>
                        <li class="disabled">Custom domain</li>
                    </ul>
                    <button class="cta-button" onclick="selectPlan('Professional')">Choose Plan</button>
                </div>
                
                <div class="pricing-card">
                    <h3 class="pricing-title">Business</h3>
                    <div class="pricing-amount">$99<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>1% transaction fee</li>
                        <li>Premium analytics</li>
                        <li>24/7 support</li>
                        <li>Advanced marketing</li>
                        <li>Affiliate program</li>
                        <li>Custom domain</li>
                    </ul>
                    <button class="cta-button outline" onclick="selectPlan('Business')">Choose Plan</button>
                </div>
            </div>
        </section>
    </div>
    
    <section class="cta-section">
        <div class="cta-container">
            <h2>Ready to Share Your Knowledge?</h2>
            <p>Join thousands of instructors earning money doing what they love. Create your first course today and start earning tomorrow.</p>
            <button class="cta-button" id="final-cta">Become an Instructor</button>
        </div>
    </section>
    
    <div class="modal" id="signup-modal">
        <div class="modal-content">
            <button class="close-modal" onclick="closeModal('signup-modal')">×</button>
            <h3>Become an Instructor</h3>
            <form id="signup-form" onsubmit="submitSignupForm(event)">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" required minlength="8">
                </div>
                <div class="form-group">
                    <label for="expertise">Your Expertise</label>
                    <select id="expertise" required>
                        <option value="">Select your expertise</option>
                        <option value="development">Web Development</option>
                        <option value="design">Design</option>
                        <option value="business">Business</option>
                        <option value="photography">Photography</option>
                        <option value="music">Music</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <button type="submit" class="cta-button" style="width: 100%;">Create Account</button>
            </form>
        </div>
    </div>
    
    <div class="modal" id="course-modal">
        <div class="modal-content">
            <button class="close-modal" onclick="closeModal('course-modal')">×</button>
            <h3 id="course-modal-title">Course Details</h3>
            <div id="course-modal-content">
                <!-- Content will be inserted by JavaScript -->
            </div>
            <button class="cta-button" style="width: 100%; margin-top: 1.5rem;" onclick="enrollInCourse()">Enroll Now</button>
        </div>
    </div>
    
    <div class="modal" id="plan-modal">
        <div class="modal-content">
            <button class="close-modal" onclick="closeModal('plan-modal')">×</button>
            <h3 id="plan-modal-title">Select Payment Method</h3>
            <form id="payment-form" onsubmit="submitPaymentForm(event)">
                <input type="hidden" id="selected-plan">
                <div class="form-group">
                    <label>Payment Method</label>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                        <label style="display: flex; align-items: center;">
                            <input type="radio" name="payment" value="credit" checked style="margin-right: 0.5rem;">
                            Credit Card
                        </label>
                        <label style="display: flex; align-items: center;">
                            <input type="radio" name="payment" value="paypal" style="margin-right: 0.5rem;">
                            PayPal
                        </label>
                    </div>
                </div>
                <div id="credit-card-fields">
                    <div class="form-group">
                        <label for="card-number">Card Number</label>
                        <input type="text" id="card-number" placeholder="1234 5678 9012 3456">
                    </div>
                    <div style="display: flex; gap: 1rem;">
                        <div class="form-group" style="flex: 1;">
                            <label for="expiry">Expiry Date</label>
                            <input type="text" id="expiry" placeholder="MM/YY">
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="cvc">CVC</label>
                            <input type="text" id="cvc" placeholder="123">
                        </div>
                    </div>
                </div>
                <button type="submit" class="cta-button" style="width: 100%;">Complete Subscription</button>
            </form>
        </div>
    </div>
    
    <div class="toast" id="toast-message"></div>
    
    <footer>
        <div class="footer-container">
            <div class="footer-about">
                <a href="#" class="footer-logo">Learn<span>Hub</span></a>
                <p>The leading platform for online course creation and sales. Empowering instructors to share knowledge and earn income.</p>
                <div class="social-links">
                    <a href="#" aria-label="Facebook">📘</a>
                    <a href="#" aria-label="Twitter">🐦</a>
                    <a href="#" aria-label="Instagram">📷</a>
                    <a href="#" aria-label="YouTube">🔴</a>
                </div>
            </div>
            
            <div class="footer-links">
                <h3>For Instructors</h3>
                <ul>
                    <li><a href="#">How It Works</a></li>
                    <li><a href="#">Pricing</a></li>
                    <li><a href="#">Course Creation</a></li>
                    <li><a href="#">Marketing Tips</a></li>
                    <li><a href="#">Success Stories</a></li>
                </ul>
            </div>
            
            <div class="footer-links">
                <h3>For Students</h3>
                <ul>
                    <li><a href="#">Browse Courses</a></li>
                    <li><a href="#">Free Courses</a></li>
                    <li><a href="#">Gift Courses</a></li>
                    <li><a href="#">Learning Paths</a></li>
                    <li><a href="#">Student Discount</a></li>
                </ul>
            </div>
            
            <div class="footer-newsletter">
                <h3>Newsletter</h3>
                <p>Subscribe to get tips and updates on course creation and online teaching.</p>
                <form class="newsletter-form" onsubmit="subscribeNewsletter(event)">
                    <input type="email" id="newsletter-email" placeholder="Your email address" required>
                    <button type="submit">→</button>
                </form>
                <p>We respect your privacy. Unsubscribe at any time.</p>
            </div>
        </div>
        
        <div class="copyright">
            &copy; 2024 LearnHub. All rights reserved. | <a href="#" style="color: white; opacity: 0.8;">Terms</a> | <a href="#" style="color: white; opacity: 0.8;">Privacy</a>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const mainNav = document.getElementById('main-nav');
        
        mobileMenuBtn.addEventListener('click', () => {
            mainNav.classList.toggle('active');
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    mainNav.classList.remove('active');
                }
            });
        });
        
        // Modal functions
        function openModal(modalId) {
            document.getElementById(modalId).style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
            document.body.style.overflow = 'auto';
        }
        
        // Close modal when clicking outside content
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
        
        // Signup button handlers
        const signupBtn = document.getElementById('signup-btn');
        const finalCta = document.getElementById('final-cta');
        
        signupBtn.addEventListener('click', () => openModal('signup-modal'));
        finalCta.addEventListener('click', () => openModal('signup-modal'));
        
        // Course modal
        function showCourseModal(courseTitle) {
            const courseModal = document.getElementById('course-modal');
            const courseModalTitle = document.getElementById('course-modal-title');
            const courseModalContent = document.getElementById('course-modal-content');
            
            courseModalTitle.textContent = courseTitle;
            
            // Generate dynamic content based on course
            let content = '';
            if (courseTitle === 'The Complete JavaScript Course 2024') {
                content = `
                    <p><strong>Category:</strong> Web Development</p>
                    <p><strong>Instructor:</strong> John Smith</p>
                    <p><strong>Price:</strong> $89.99</p>
                    <p><strong>Rating:</strong> ★ 4.8 (1,245 students)</p>
                    <p style="margin-top: 1rem;">Master JavaScript with this complete course from beginner to advanced levels. Learn modern JavaScript (ES6+) through real-world projects and challenges.</p>
                    <h4 style="margin: 1.5rem 0 0.5rem;">What you'll learn:</h4>
                    <ul style="padding-left: 1.5rem;">
                        <li>JavaScript fundamentals</li>
                        <li>DOM manipulation</li>
                        <li>Async programming</li>
                        <li>Modern ES6+ features</li>
                        <li>Real-world projects</li>
                    </ul>
                `;
            } else if (courseTitle === 'Python for Data Analysis') {
                content = `
                    <p><strong>Category:</strong> Data Science</p>
                    <p><strong>Instructor:</strong> Sarah Johnson</p>
                    <p><strong>Price:</strong> $79.99</p>
                    <p><strong>Rating:</strong> ★ 4.7 (892 students)</p>
                    <p style="margin-top: 1rem;">Learn how to use Python for data analysis and visualization with Pandas, NumPy, Matplotlib, and Seaborn.</p>
                    <h4 style="margin: 1.5rem 0 0.5rem;">What you'll learn:</h4>
                    <ul style="padding-left: 1.5rem;">
                        <li>Data cleaning techniques</li>
                        <li>Exploratory data analysis</li>
                        <li>Data visualization</li>
                        <li>Statistical analysis</li>
                        <li>Real-world case studies</li>
                    </ul>
                `;
            } else if (courseTitle === 'Digital Photography Masterclass') {
                content = `
                    <p><strong>Category:</strong> Photography</p>
                    <p><strong>Instructor:</strong> Michael Brown</p>
                    <p><strong>Price:</strong> $69.99</p>
                    <p><strong>Rating:</strong> ★ 4.9 (2,103 students)</p>
                    <p style="margin-top: 1rem;">A complete guide to digital photography from camera basics to advanced composition techniques.</p>
                    <h4 style="margin: 1.5rem 0 0.5rem;">What you'll learn:</h4>
                    <ul style="padding-left: 1.5rem;">
                        <li>Camera settings and modes</li>
                        <li>Lighting techniques</li>
                        <li>Composition rules</li>
                        <li>Photo editing basics</li>
                        <li>Building a portfolio</li>
                    </ul>
                `;
            }
            
            courseModalContent.innerHTML = content;
            openModal('course-modal');
        }
        
        function enrollInCourse() {
            closeModal('course-modal');
            showToast('Course enrollment successful!');
        }
        
        // Plan selection
        function selectPlan(planName) {
            document.getElementById('selected-plan').value = planName;
            document.getElementById('plan-modal-title').textContent = `Subscribe to ${planName} Plan`;
            openModal('plan-modal');
        }
        
        // Form submissions
        function submitSignupForm(e) {
            e.preventDefault();
            closeModal('signup-modal');
            showToast('Account created successfully! Welcome to LearnHub.');
            // In a real app, you would send this data to your backend
            console.log('Signup form submitted:', {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                expertise: document.getElementById('expertise').value
            });
        }
        
        function submitPaymentForm(e) {
            e.preventDefault();
            closeModal('plan-modal');
            const plan = document.getElementById('selected-plan').value;
            showToast(`Thank you for subscribing to our ${plan} plan!`);
            // In a real app, you would process payment here
            console.log('Payment form submitted for plan:', plan);
        }
        
        function subscribeNewsletter(e) {
            e.preventDefault();
            const email = document.getElementById('newsletter-email').value;
            showToast('Thanks for subscribing to our newsletter!');
            // In a real app, you would send this email to your mailing list
            console.log('Newsletter subscription:', email);
            document.getElementById('newsletter-email').value = '';
        }
        
        // Toast notification
        function showToast(message) {
            const toast = document.getElementById('toast-message');
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    # Here you would typically save to database
    return jsonify({'status': 'success', 'message': 'Account created successfully'})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    # Here you would typically process payment
    return jsonify({'status': 'success', 'message': 'Subscription successful'})

@app.route('/api/newsletter', methods=['POST'])
def newsletter():
    data = request.json
    # Here you would typically add to mailing list
    return jsonify({'status': 'success', 'message': 'Newsletter subscription successful'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)