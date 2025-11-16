# SEO Optimization Module for AdmitionWala
# Improves search engine rankings and visibility
# Includes meta tags, schema markup, and SEO best practices

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.conf import settings


SEO_KEYWORDS = {
    'home': [
        'colleges in India',
        'college admissions',
        'education platform',
        'college recommendations',
        'stream selection guidance',
        'engineering colleges',
        'medical colleges',
        'MBA colleges',
        'college rankings',
        'student reviews',
        'career guidance',
        'college counseling',
        'apply to colleges online',
        'college comparison'
    ],
    'colleges': [
        'find colleges',
        'college search',
        'top colleges India',
        'college locations',
        'college courses',
        'engineering colleges',
        'medical colleges',
        'arts colleges',
        'commerce colleges',
        'college fees',
        'college reviews',
        'college admissions'
    ],
    'courses': [
        'courses available',
        'engineering courses',
        'medical courses',
        'MBA programs',
        'stream selection',
        'course details',
        'course eligibility',
        'course duration',
        'course fees',
        'course syllabus'
    ],
    'careers': [
        'job opportunities',
        'career guidance',
        'job placements',
        'internships',
        'career development',
        'job search',
        'company profiles',
        'career paths',
        'skill development',
        'employment opportunities'
    ]
}

SEO_DESCRIPTIONS = {
    'home': 'Find the best colleges for your future with AdmitionWala. Search 1000+ colleges, get personalized recommendations, and apply through our easy-to-use platform. Expert counseling available 24/7.',
    'colleges': 'Explore comprehensive college information including courses, fees, reviews, and placements. Find your perfect college match with our advanced search and filtering options.',
    'courses': 'Discover various courses and programs offered by colleges across India. Compare course details, eligibility criteria, duration, and fees.',
    'careers': 'Explore career opportunities and job openings across leading companies. Get career guidance and placement assistance from industry experts.',
    'counseling': 'Get personalized counseling from our AI-powered advisor. Receive guidance in your preferred language on college selection and career paths.'
}


class SEOOptimizer:
    """Handles SEO optimization for the website"""
    
    @staticmethod
    def get_meta_tags(page_name, title='', description=''):
        """Generate meta tags for a page"""
        keywords = SEO_KEYWORDS.get(page_name, [])
        desc = description or SEO_DESCRIPTIONS.get(page_name, '')
        
        meta_tags = {
            'title': title or f'{page_name.title()} - AdmitionWala',
            'description': desc,
            'keywords': ', '.join(keywords),
            'og:title': title or f'{page_name.title()} - AdmitionWala',
            'og:description': desc,
            'og:type': 'website',
            'twitter:card': 'summary_large_image',
            'twitter:title': title or f'{page_name.title()} - AdmitionWala',
            'twitter:description': desc,
            'canonical': f'https://admitionwala.com/{page_name}/'
        }
        return meta_tags

    @staticmethod
    def get_schema_markup(content_type='Organization', data=None):
        """Generate JSON-LD schema markup for SEO"""
        schemas = {
            'Organization': {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "AdmitionWala",
                "description": "Your gateway to quality education and career opportunities in India",
                "url": "https://admitionwala.com",
                "logo": "https://admitionwala.com/static/images/admitionwala_logo.svg",
                "sameAs": [
                    "https://www.facebook.com/admitionwala",
                    "https://www.twitter.com/admitionwala",
                    "https://www.instagram.com/admitionwala",
                    "https://www.linkedin.com/company/admitionwala"
                ],
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "Customer Service",
                    "email": "support@admitionwala.com"
                }
            },
            'BreadcrumbList': {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://admitionwala.com"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": data.get('name', '') if data else '',
                        "item": data.get('url', '') if data else ''
                    }
                ]
            },
            'LocalBusiness': {
                "@context": "https://schema.org",
                "@type": "LocalBusiness",
                "name": "AdmitionWala",
                "image": "https://admitionwala.com/static/images/admitionwala_logo.svg",
                "description": "Educational guidance platform providing college counseling and career opportunities",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "India",
                    "addressCountry": "IN"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.8",
                    "ratingCount": "5000+"
                }
            }
        }
        
        return schemas.get(content_type, schemas['Organization'])

    @staticmethod
    def generate_sitemap_entry(url, priority=0.8, changefreq='weekly'):
        """Generate XML sitemap entry"""
        return f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{__import__('datetime').datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
"""


def robots_txt_content():
    """Generate robots.txt content for SEO"""
    return """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/admin/
Disallow: /static/images/temp/

# Crawl delay for better server performance
Crawl-delay: 1

# Sitemaps
Sitemap: https://admitionwala.com/sitemap.xml

# Social media bots
User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: WhatsApp
Allow: /

User-agent: Telegram
Allow: /
"""


def generate_open_graph_tags(title, description, image_url, url):
    """Generate Open Graph meta tags for social sharing"""
    tags = f"""<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{image_url}" />
<meta property="og:url" content="{url}" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{image_url}" />"""
    return tags


def generate_structured_data_for_college(college):
    """Generate structured data for a college"""
    return {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": college.name,
        "description": college.description,
        "url": college.website,
        "image": college.logo.url if college.logo else None,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": college.location,
            "addressCountry": "India"
        },
        "potentialAction": {
            "@type": "EnrollAction",
            "target": f"https://admitionwala.com/college/{college.id}/"
        }
    }


# SEO Checklist for best practices
SEO_CHECKLIST = {
    'Meta Tags': [
        'Title tag (50-60 characters)',
        'Meta description (150-160 characters)',
        'Meta keywords (5-7 main keywords)',
        'Open Graph tags for social sharing',
        'Twitter Card tags'
    ],
    'Content': [
        'Unique and original content',
        'Proper heading hierarchy (H1, H2, H3)',
        'Natural keyword placement',
        'Image alt text',
        'Internal linking'
    ],
    'Technical': [
        'Mobile-friendly design',
        'Fast page load speed',
        'SSL/HTTPS enabled',
        'XML sitemap',
        'Robots.txt'
    ],
    'Accessibility': [
        'Semantic HTML',
        'ARIA labels',
        'Keyboard navigation',
        'Color contrast',
        'Text alternatives'
    ]
}
