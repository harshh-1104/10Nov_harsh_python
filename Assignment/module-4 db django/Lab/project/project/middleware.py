import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class AppNavigationMiddleware(MiddlewareMixin):
    # Maintain the order of applications as they appear on the home page
    APP_ROUTES = [
        ('/q1/', 'Q1'),
        ('/q2/', 'Q2'),
        ('/q3/', 'Q3'),
        ('/q4/', 'Q4'),
        ('/q6/', 'Q6'),
        ('/q7/', 'Q7'),
        ('/q9/', 'Q9'),
        ('/q10/', 'Q10'),
        ('/q11/', 'Q11'),
        ('/q12/', 'Q12'),
        ('/q13/', 'Q13'),
        ('/q14/', 'Q14'),
        ('/q16/', 'Q16'),
        ('/q17_18_19/', 'Q17_18_19'),
        ('/q20/', 'Q20'),
    ]

    def process_response(self, request, response):
        # We only want to inject HTML into text/html responses
        if response.get('Content-Type', '').startswith('text/html'):
            path = request.path
            current_app_idx = -1
            
            # Skip for the home page or admin
            if path == '/' or path.startswith('/admin/'):
                return response
                
            # Find out which app we are currently navigating
            for i, (app_url, app_name) in enumerate(self.APP_ROUTES):
                if path.startswith(app_url):
                    current_app_idx = i
                    break
            
            # If we are inside one of the apps, inject the navigation buttons
            if current_app_idx != -1:
                prev_url = self.APP_ROUTES[current_app_idx - 1][0] if current_app_idx > 0 else None
                next_url = self.APP_ROUTES[current_app_idx + 1][0] if current_app_idx < len(self.APP_ROUTES) - 1 else None
                
                buttons_html = """
<style>
    .global-app-navigation {
        position: fixed;
        z-index: 10000;
        pointer-events: none;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
    }
    .nav-btn {
        pointer-events: auto;
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        color: #fff;
        text-decoration: none;
        font-size: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        opacity: 0.9;
        border: 2px solid rgba(255, 255, 255, 0.5);
    }
    .nav-btn:hover {
        opacity: 1;
        transform: translateY(-50%) scale(1.15);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.6);
        color: #fff;
    }
    
    /* Vibrant colors for the arrows */
    .nav-prev { 
        left: 20px; 
        background: linear-gradient(135deg, #ff416c, #ff4b2b); /* Fiery red/orange */
    }
    .nav-next { 
        right: 20px; 
        background: linear-gradient(135deg, #11998e, #38ef7d); /* Vibrant green */
    }
    
    .nav-prev:hover {
        background: linear-gradient(135deg, #ff4b2b, #ff416c);
    }
    .nav-next:hover {
        background: linear-gradient(135deg, #38ef7d, #11998e);
    }

    @media (prefers-color-scheme: light) {
        .nav-btn {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.5);
        }
    }
    .nav-home {
        pointer-events: auto;
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 10px 20px;
        background: #007bff;
        color: white !important;
        text-decoration: none;
        border-radius: 30px;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,123,255,0.4);
        transition: all 0.3s ease;
        border: none;
    }
    .nav-home:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,123,255,0.6);
        background: #0056b3;
    }
</style>
<div class="global-app-navigation">
"""
                if prev_url:
                    buttons_html += f'    <a href="{prev_url}" class="nav-btn nav-prev" title="Previous App">&#10094;</a>\n'
                if next_url:
                    buttons_html += f'    <a href="{next_url}" class="nav-btn nav-next" title="Next App">&#10095;</a>\n'
                
                buttons_html += '    <a href="/" class="nav-home" title="Home">🏠 Home</a>\n</div>\n'

                try:
                    content = response.content.decode(response.charset or 'utf-8')
                    # Insert the HTML just before the closing body tag
                    body_end_idx = content.rfind('</body>')
                    if body_end_idx != -1:
                        content = content[:body_end_idx] + buttons_html + content[body_end_idx:]
                        response.content = content.encode(response.charset or 'utf-8')
                        if 'Content-Length' in response:
                            response['Content-Length'] = str(len(response.content))
                except Exception:
                    # In case decoding fails, gracefully skip modifying the response
                    pass

        return response
