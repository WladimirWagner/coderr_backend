from django.contrib.auth.models import User
from coderr_app.models import Profile, Offer, OfferDetail, Order, Review


# Users erstellen
user1, _ = User.objects.get_or_create(username='max_business', email='max@business.de')
user1.set_password('asdasd')
user1.save()

user2, _ = User.objects.get_or_create(username='jane_business', email='jane@business.de')
user2.set_password('asdasd')
user2.save()

user3, _ = User.objects.get_or_create(username='john_customer', email='john@customer.de')
user3.set_password('asdasd')
user3.save()

user4, _ = User.objects.get_or_create(username='sarah_customer', email='sarah@customer.de')
user4.set_password('asdasd')
user4.save()

user5, _ = User.objects.get_or_create(username='admin', email='admin@coderr.de', is_staff=True)
user5.set_password('asdasd')
user5.save()

# Zusätzliche Business Users
user6, _ = User.objects.get_or_create(username='alex_business', email='alex@business.de')
user6.set_password('asdasd')
user6.save()

user7, _ = User.objects.get_or_create(username='lisa_business', email='lisa@business.de')
user7.set_password('asdasd')
user7.save()

user8, _ = User.objects.get_or_create(username='tom_business', email='tom@business.de')
user8.set_password('asdasd')
user8.save()

# Zusätzliche Customer Users
user9, _ = User.objects.get_or_create(username='emma_customer', email='emma@customer.de')
user9.set_password('asdasd')
user9.save()

user10, _ = User.objects.get_or_create(username='mike_customer', email='mike@customer.de')
user10.set_password('asdasd')
user10.save()

user11, _ = User.objects.get_or_create(username='anna_customer', email='anna@customer.de')
user11.set_password('asdasd')
user11.save()

user12, _ = User.objects.get_or_create(username='david_customer', email='david@customer.de')
user12.set_password('asdasd')
user12.save()


# Profiles erstellen
profile1, _ = Profile.objects.get_or_create(
    username=user1,
    defaults={
        'first_name': 'Max',
        'last_name': 'Mustermann',
        'location': 'Berlin',
        'tel': '0123456789',
        'description': 'Professioneller Webdesigner mit 5 Jahren Erfahrung',
        'working_hours': '9-17 Uhr',
        'type': 'business',
        'email': 'max@business.de'
    }
)

profile2, _ = Profile.objects.get_or_create(
    username=user2,
    defaults={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'location': 'Hamburg',
        'tel': '0987654321',
        'description': 'Grafikdesignerin spezialisiert auf Logo-Design',
        'working_hours': '10-18 Uhr',
        'type': 'business',
        'email': 'jane@business.de'
    }
)

profile3, _ = Profile.objects.get_or_create(
    username=user3,
    defaults={
        'first_name': 'John',
        'last_name': 'Smith',
        'location': 'München',
        'tel': '0555123456',
        'description': 'Kunde auf der Suche nach qualitativ hochwertigen Dienstleistungen',
        'working_hours': '',
        'type': 'customer',
        'email': 'john@customer.de'
    }
)

profile4, _ = Profile.objects.get_or_create(
    username=user4,
    defaults={
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'location': 'Köln',
        'tel': '0555987654',
        'description': 'Kundin mit verschiedenen Projektanforderungen',
        'working_hours': '',
        'type': 'customer',
        'email': 'sarah@customer.de'
    }
)

# Zusätzliche Business Profiles
profile6, _ = Profile.objects.get_or_create(
    username=user6,
    defaults={
        'first_name': 'Alex',
        'last_name': 'Weber',
        'location': 'Frankfurt',
        'tel': '0123456780',
        'description': 'Mobile App Entwickler mit Fokus auf iOS und Android',
        'working_hours': '8-16 Uhr',
        'type': 'business',
        'email': 'alex@business.de'
    }
)

profile7, _ = Profile.objects.get_or_create(
    username=user7,
    defaults={
        'first_name': 'Lisa',
        'last_name': 'Müller',
        'location': 'Stuttgart',
        'tel': '0123456781',
        'description': 'Content Creator und Social Media Manager',
        'working_hours': '9-18 Uhr',
        'type': 'business',
        'email': 'lisa@business.de'
    }
)

profile8, _ = Profile.objects.get_or_create(
    username=user8,
    defaults={
        'first_name': 'Tom',
        'last_name': 'Schmidt',
        'location': 'Düsseldorf',
        'tel': '0123456782',
        'description': 'SEO-Spezialist und Digital Marketing Experte',
        'working_hours': '10-19 Uhr',
        'type': 'business',
        'email': 'tom@business.de'
    }
)

# Zusätzliche Customer Profiles
profile9, _ = Profile.objects.get_or_create(
    username=user9,
    defaults={
        'first_name': 'Emma',
        'last_name': 'Brown',
        'location': 'Dortmund',
        'tel': '0555123457',
        'description': 'Startup-Gründerin auf der Suche nach professionellen Dienstleistungen',
        'working_hours': '',
        'type': 'customer',
        'email': 'emma@customer.de'
    }
)

profile10, _ = Profile.objects.get_or_create(
    username=user10,
    defaults={
        'first_name': 'Mike',
        'last_name': 'Davis',
        'location': 'Leipzig',
        'tel': '0555123458',
        'description': 'Kleingewerbetreibender mit digitalen Anforderungen',
        'working_hours': '',
        'type': 'customer',
        'email': 'mike@customer.de'
    }
)

profile11, _ = Profile.objects.get_or_create(
    username=user11,
    defaults={
        'first_name': 'Anna',
        'last_name': 'Wilson',
        'location': 'Bremen',
        'tel': '0555123459',
        'description': 'Freelancerin mit verschiedenen Projektanforderungen',
        'working_hours': '',
        'type': 'customer',
        'email': 'anna@customer.de'
    }
)

profile12, _ = Profile.objects.get_or_create(
    username=user12,
    defaults={
        'first_name': 'David',
        'last_name': 'Taylor',
        'location': 'Hannover',
        'tel': '0555123460',
        'description': 'Student mit kreativen Projektideen',
        'working_hours': '',
        'type': 'customer',
        'email': 'david@customer.de'
    }
)


# Offers erstellen
offer1 = Offer.objects.create(
    user=profile1,
    title='Professionelles Webdesign-Paket',
    description='Ein umfassendes Webdesign-Paket für Unternehmen, das moderne und responsive Websites erstellt.'
)

offer2 = Offer.objects.create(
    user=profile2,
    title='Logo-Design & Branding',
    description='Professionelle Logo-Designs und Branding-Lösungen für Ihr Unternehmen.'
)

offer3 = Offer.objects.create(
    user=profile1,
    title='E-Commerce Website Entwicklung',
    description='Vollständige E-Commerce-Lösungen mit modernen Zahlungssystemen.'
)

offer4 = Offer.objects.create(
    user=profile6,
    title='Mobile App Entwicklung',
    description='Native und Cross-Platform Mobile Apps für iOS und Android.'
)

offer5 = Offer.objects.create(
    user=profile7,
    title='Social Media Management',
    description='Professionelles Social Media Management und Content Creation.'
)

offer6 = Offer.objects.create(
    user=profile8,
    title='SEO & Digital Marketing',
    description='Umfassende SEO-Optimierung und Digital Marketing Strategien.'
)

offer7 = Offer.objects.create(
    user=profile2,
    title='Print Design & Layout',
    description='Professionelle Print-Designs für Flyer, Broschüren und Magazine.'
)

offer8 = Offer.objects.create(
    user=profile6,
    title='Web App Entwicklung',
    description='Moderne Web-Anwendungen mit React, Vue.js und Node.js.'
)

offer9 = Offer.objects.create(
    user=profile7,
    title='Video Production & Editing',
    description='Professionelle Videoproduktion und Post-Production Services.'
)

offer10 = Offer.objects.create(
    user=profile8,
    title='Analytics & Reporting',
    description='Detaillierte Analytics-Berichte und Performance-Optimierung.'
)


# OfferDetails erstellen
detail1_basic = OfferDetail.objects.create(
    offer=offer1,
    title='Basic Webdesign',
    revisions=2,
    delivery_time_in_days=5,
    price=500.00,
    features=['Responsive Design', '3 Seiten', 'Kontaktformular'],
    offer_type='basic'
)

detail1_standard = OfferDetail.objects.create(
    offer=offer1,
    title='Standard Webdesign',
    revisions=5,
    delivery_time_in_days=10,
    price=1000.00,
    features=['Responsive Design', '5 Seiten', 'Kontaktformular', 'SEO-Optimierung'],
    offer_type='standard'
)

detail1_premium = OfferDetail.objects.create(
    offer=offer1,
    title='Premium Webdesign',
    revisions=10,
    delivery_time_in_days=15,
    price=2000.00,
    features=['Responsive Design', '10 Seiten', 'Kontaktformular', 'SEO-Optimierung', 'CMS-Integration'],
    offer_type='premium'
)

detail2_basic = OfferDetail.objects.create(
    offer=offer2,
    title='Basic Logo Design',
    revisions=3,
    delivery_time_in_days=3,
    price=200.00,
    features=['Logo Design', '2 Revisionen', 'PNG & JPG Format'],
    offer_type='basic'
)

detail2_standard = OfferDetail.objects.create(
    offer=offer2,
    title='Standard Logo Design',
    revisions=5,
    delivery_time_in_days=5,
    price=400.00,
    features=['Logo Design', '5 Revisionen', 'Alle Formate', 'Brand Guidelines'],
    offer_type='standard'
)

detail2_premium = OfferDetail.objects.create(
    offer=offer2,
    title='Premium Logo Design',
    revisions=10,
    delivery_time_in_days=7,
    price=800.00,
    features=['Logo Design', '10 Revisionen', 'Alle Formate', 'Brand Guidelines', 'Social Media Kit'],
    offer_type='premium'
)

detail3_basic = OfferDetail.objects.create(
    offer=offer3,
    title='Basic E-Commerce',
    revisions=3,
    delivery_time_in_days=14,
    price=1500.00,
    features=['E-Commerce Website', 'Produktkatalog', 'Warenkorb'],
    offer_type='basic'
)

detail3_standard = OfferDetail.objects.create(
    offer=offer3,
    title='Standard E-Commerce',
    revisions=5,
    delivery_time_in_days=21,
    price=3000.00,
    features=['E-Commerce Website', 'Produktkatalog', 'Warenkorb', 'Zahlungsintegration', 'Admin-Panel'],
    offer_type='standard'
)

detail3_premium = OfferDetail.objects.create(
    offer=offer3,
    title='Premium E-Commerce',
    revisions=10,
    delivery_time_in_days=30,
    price=6000.00,
    features=['E-Commerce Website', 'Produktkatalog', 'Warenkorb', 'Zahlungsintegration', 'Admin-Panel', 'Analytics', 'Marketing-Tools'],
    offer_type='premium'
)

detail4_basic = OfferDetail.objects.create(
    offer=offer4,
    title='Basic Mobile App',
    revisions=3,
    delivery_time_in_days=21,
    price=2000.00,
    features=['Native App', 'iOS/Android', 'Basis-Features'],
    offer_type='basic'
)

detail4_standard = OfferDetail.objects.create(
    offer=offer4,
    title='Standard Mobile App',
    revisions=5,
    delivery_time_in_days=35,
    price=4000.00,
    features=['Native App', 'iOS/Android', 'Erweiterte Features', 'Backend-Integration'],
    offer_type='standard'
)

detail4_premium = OfferDetail.objects.create(
    offer=offer4,
    title='Premium Mobile App',
    revisions=10,
    delivery_time_in_days=50,
    price=8000.00,
    features=['Native App', 'iOS/Android', 'Alle Features', 'Backend-Integration', 'Analytics', 'Push-Notifications'],
    offer_type='premium'
)

detail5_basic = OfferDetail.objects.create(
    offer=offer5,
    title='Basic Social Media',
    revisions=2,
    delivery_time_in_days=7,
    price=300.00,
    features=['Content Creation', '3 Posts/Woche', '2 Plattformen'],
    offer_type='basic'
)

detail5_standard = OfferDetail.objects.create(
    offer=offer5,
    title='Standard Social Media',
    revisions=5,
    delivery_time_in_days=14,
    price=600.00,
    features=['Content Creation', '5 Posts/Woche', '4 Plattformen', 'Community Management'],
    offer_type='standard'
)

detail5_premium = OfferDetail.objects.create(
    offer=offer5,
    title='Premium Social Media',
    revisions=10,
    delivery_time_in_days=21,
    price=1200.00,
    features=['Content Creation', '7 Posts/Woche', 'Alle Plattformen', 'Community Management', 'Paid Ads'],
    offer_type='premium'
)

detail6_basic = OfferDetail.objects.create(
    offer=offer6,
    title='Basic SEO',
    revisions=2,
    delivery_time_in_days=14,
    price=400.00,
    features=['On-Page SEO', 'Keyword-Analyse', 'Basis-Optimierung'],
    offer_type='basic'
)

detail6_standard = OfferDetail.objects.create(
    offer=offer6,
    title='Standard SEO',
    revisions=5,
    delivery_time_in_days=28,
    price=800.00,
    features=['On-Page SEO', 'Off-Page SEO', 'Keyword-Analyse', 'Content-Strategie'],
    offer_type='standard'
)

detail6_premium = OfferDetail.objects.create(
    offer=offer6,
    title='Premium SEO',
    revisions=10,
    delivery_time_in_days=42,
    price=1600.00,
    features=['Vollständige SEO', 'Content-Marketing', 'Link-Building', 'Analytics', 'Reporting'],
    offer_type='premium'
)

detail7_basic = OfferDetail.objects.create(
    offer=offer7,
    title='Basic Print Design',
    revisions=2,
    delivery_time_in_days=3,
    price=150.00,
    features=['Flyer Design', '2 Revisionen', 'Print-Ready Files'],
    offer_type='basic'
)

detail7_standard = OfferDetail.objects.create(
    offer=offer7,
    title='Standard Print Design',
    revisions=5,
    delivery_time_in_days=7,
    price=300.00,
    features=['Flyer & Broschüren', '5 Revisionen', 'Print-Ready Files', 'Brand Guidelines'],
    offer_type='standard'
)

detail7_premium = OfferDetail.objects.create(
    offer=offer7,
    title='Premium Print Design',
    revisions=10,
    delivery_time_in_days=14,
    price=600.00,
    features=['Komplettes Print-Set', '10 Revisionen', 'Print-Ready Files', 'Brand Guidelines', 'Mockups'],
    offer_type='premium'
)

detail8_basic = OfferDetail.objects.create(
    offer=offer8,
    title='Basic Web App',
    revisions=3,
    delivery_time_in_days=21,
    price=1500.00,
    features=['Web App', 'Basis-Features', 'Responsive Design'],
    offer_type='basic'
)

detail8_standard = OfferDetail.objects.create(
    offer=offer8,
    title='Standard Web App',
    revisions=5,
    delivery_time_in_days=35,
    price=3000.00,
    features=['Web App', 'Erweiterte Features', 'Database-Integration', 'User-Authentication'],
    offer_type='standard'
)

detail8_premium = OfferDetail.objects.create(
    offer=offer8,
    title='Premium Web App',
    revisions=10,
    delivery_time_in_days=50,
    price=6000.00,
    features=['Web App', 'Alle Features', 'Database-Integration', 'User-Authentication', 'API', 'Analytics'],
    offer_type='premium'
)

detail9_basic = OfferDetail.objects.create(
    offer=offer9,
    title='Basic Video Production',
    revisions=2,
    delivery_time_in_days=7,
    price=500.00,
    features=['Video Editing', '2 Minuten', 'HD Quality'],
    offer_type='basic'
)

detail9_standard = OfferDetail.objects.create(
    offer=offer9,
    title='Standard Video Production',
    revisions=5,
    delivery_time_in_days=14,
    price=1000.00,
    features=['Video Production', '5 Minuten', '4K Quality', 'Color Grading'],
    offer_type='standard'
)

detail9_premium = OfferDetail.objects.create(
    offer=offer9,
    title='Premium Video Production',
    revisions=10,
    delivery_time_in_days=21,
    price=2000.00,
    features=['Video Production', '10 Minuten', '4K Quality', 'Color Grading', 'Motion Graphics', 'Sound Design'],
    offer_type='premium'
)

detail10_basic = OfferDetail.objects.create(
    offer=offer10,
    title='Basic Analytics',
    revisions=2,
    delivery_time_in_days=7,
    price=200.00,
    features=['Google Analytics Setup', 'Basis-Reporting', 'Monthly Reports'],
    offer_type='basic'
)

detail10_standard = OfferDetail.objects.create(
    offer=offer10,
    title='Standard Analytics',
    revisions=5,
    delivery_time_in_days=14,
    price=400.00,
    features=['Analytics Setup', 'Custom Reporting', 'Weekly Reports', 'Performance-Optimierung'],
    offer_type='standard'
)

detail10_premium = OfferDetail.objects.create(
    offer=offer10,
    title='Premium Analytics',
    revisions=10,
    delivery_time_in_days=21,
    price=800.00,
    features=['Vollständige Analytics', 'Custom Dashboards', 'Daily Reports', 'Performance-Optimierung', 'A/B Testing'],
    offer_type='premium'
)


# Orders erstellen
order1 = Order.objects.create(
    customer_user=profile3,
    business_user=profile1,
    offer_detail=detail1_standard,
    title='Standard Webdesign',
    revisions=5,
    delivery_time_in_days=10,
    price=1000.00,
    features=['Responsive Design', '5 Seiten', 'Kontaktformular', 'SEO-Optimierung'],
    offer_type='standard',
    status='in_progress'
)

order2 = Order.objects.create(
    customer_user=profile4,
    business_user=profile2,
    offer_detail=detail2_premium,
    title='Premium Logo Design',
    revisions=10,
    delivery_time_in_days=7,
    price=800.00,
    features=['Logo Design', '10 Revisionen', 'Alle Formate', 'Brand Guidelines', 'Social Media Kit'],
    offer_type='premium',
    status='completed'
)

order3 = Order.objects.create(
    customer_user=profile3,
    business_user=profile1,
    offer_detail=detail3_basic,
    title='Basic E-Commerce',
    revisions=3,
    delivery_time_in_days=14,
    price=1500.00,
    features=['E-Commerce Website', 'Produktkatalog', 'Warenkorb'],
    offer_type='basic',
    status='in_progress'
)

order4 = Order.objects.create(
    customer_user=profile4,
    business_user=profile2,
    offer_detail=detail1_basic,
    title='Basic Webdesign',
    revisions=2,
    delivery_time_in_days=5,
    price=500.00,
    features=['Responsive Design', '3 Seiten', 'Kontaktformular'],
    offer_type='basic',
    status='cancelled'
)

order5 = Order.objects.create(
    customer_user=profile9,
    business_user=profile6,
    offer_detail=detail4_standard,
    title='Standard Mobile App',
    revisions=5,
    delivery_time_in_days=35,
    price=4000.00,
    features=['Native App', 'iOS/Android', 'Erweiterte Features', 'Backend-Integration'],
    offer_type='standard',
    status='completed'
)

order6 = Order.objects.create(
    customer_user=profile10,
    business_user=profile7,
    offer_detail=detail5_basic,
    title='Basic Social Media',
    revisions=2,
    delivery_time_in_days=7,
    price=300.00,
    features=['Content Creation', '3 Posts/Woche', '2 Plattformen'],
    offer_type='basic',
    status='in_progress'
)

order7 = Order.objects.create(
    customer_user=profile11,
    business_user=profile8,
    offer_detail=detail6_premium,
    title='Premium SEO',
    revisions=10,
    delivery_time_in_days=42,
    price=1600.00,
    features=['Vollständige SEO', 'Content-Marketing', 'Link-Building', 'Analytics', 'Reporting'],
    offer_type='premium',
    status='completed'
)

order8 = Order.objects.create(
    customer_user=profile12,
    business_user=profile2,
    offer_detail=detail7_standard,
    title='Standard Print Design',
    revisions=5,
    delivery_time_in_days=7,
    price=300.00,
    features=['Flyer & Broschüren', '5 Revisionen', 'Print-Ready Files', 'Brand Guidelines'],
    offer_type='standard',
    status='in_progress'
)

order9 = Order.objects.create(
    customer_user=profile9,
    business_user=profile6,
    offer_detail=detail8_basic,
    title='Basic Web App',
    revisions=3,
    delivery_time_in_days=21,
    price=1500.00,
    features=['Web App', 'Basis-Features', 'Responsive Design'],
    offer_type='basic',
    status='completed'
)

order10 = Order.objects.create(
    customer_user=profile10,
    business_user=profile7,
    offer_detail=detail9_premium,
    title='Premium Video Production',
    revisions=10,
    delivery_time_in_days=21,
    price=2000.00,
    features=['Video Production', '10 Minuten', '4K Quality', 'Color Grading', 'Motion Graphics', 'Sound Design'],
    offer_type='premium',
    status='in_progress'
)

order11 = Order.objects.create(
    customer_user=profile11,
    business_user=profile8,
    offer_detail=detail10_standard,
    title='Standard Analytics',
    revisions=5,
    delivery_time_in_days=14,
    price=400.00,
    features=['Analytics Setup', 'Custom Reporting', 'Weekly Reports', 'Performance-Optimierung'],
    offer_type='standard',
    status='completed'
)

order12 = Order.objects.create(
    customer_user=profile12,
    business_user=profile1,
    offer_detail=detail1_premium,
    title='Premium Webdesign',
    revisions=10,
    delivery_time_in_days=15,
    price=2000.00,
    features=['Responsive Design', '10 Seiten', 'Kontaktformular', 'SEO-Optimierung', 'CMS-Integration'],
    offer_type='premium',
    status='cancelled'
)

order13 = Order.objects.create(
    customer_user=profile3,
    business_user=profile6,
    offer_detail=detail4_basic,
    title='Basic Mobile App',
    revisions=3,
    delivery_time_in_days=21,
    price=2000.00,
    features=['Native App', 'iOS/Android', 'Basis-Features'],
    offer_type='basic',
    status='completed'
)


# Reviews erstellen
review1 = Review.objects.create(
    business_user=profile1,
    reviewer=profile3,
    rating=5,
    description='Ausgezeichnete Arbeit! Max hat meine Website genau nach meinen Vorstellungen erstellt. Sehr professionell und zuverlässig.'
)

review2 = Review.objects.create(
    business_user=profile2,
    reviewer=profile4,
    rating=4,
    description='Sehr gute Logo-Designs. Jane hat meine Marke perfekt verstanden und umgesetzt. Empfehlung!'
)

review3 = Review.objects.create(
    business_user=profile1,
    reviewer=profile4,
    rating=5,
    description='Max ist ein echter Profi! Die E-Commerce-Lösung funktioniert perfekt und die Kunden sind begeistert.'
)

review4 = Review.objects.create(
    business_user=profile2,
    reviewer=profile3,
    rating=4,
    description='Jane hat ein wunderschönes Logo für mein Unternehmen erstellt. Sehr kreativ und professionell.'
)

review5 = Review.objects.create(
    business_user=profile1,
    reviewer=profile4,
    rating=5,
    description='Beste Webdesign-Erfahrung! Max hat meine Vision perfekt umgesetzt und die Website übertrifft alle Erwartungen.'
)

review6 = Review.objects.create(
    business_user=profile6,
    reviewer=profile9,
    rating=5,
    description='Alex hat eine fantastische Mobile App entwickelt! Die Benutzerfreundlichkeit ist hervorragend und die Performance ist top.'
)

review7 = Review.objects.create(
    business_user=profile7,
    reviewer=profile10,
    rating=4,
    description='Lisa hat unsere Social Media Präsenz komplett transformiert. Die Inhalte sind kreativ und engagierend.'
)

review8 = Review.objects.create(
    business_user=profile8,
    reviewer=profile11,
    rating=5,
    description='Tom hat unsere SEO-Performance dramatisch verbessert. Die Rankings sind gestiegen und der Traffic hat sich verdoppelt.'
)

review9 = Review.objects.create(
    business_user=profile2,
    reviewer=profile12,
    rating=4,
    description='Jane hat wunderschöne Print-Designs für unser Unternehmen erstellt. Die Qualität ist erstklassig.'
)

review10 = Review.objects.create(
    business_user=profile6,
    reviewer=profile9,
    rating=5,
    description='Alex ist ein echter Experte für Web-Apps. Die Anwendung funktioniert einwandfrei und ist sehr benutzerfreundlich.'
)

review11 = Review.objects.create(
    business_user=profile7,
    reviewer=profile10,
    rating=5,
    description='Lisa hat ein fantastisches Video für uns produziert. Die Qualität ist professionell und die Kreativität ist beeindruckend.'
)

review12 = Review.objects.create(
    business_user=profile8,
    reviewer=profile11,
    rating=4,
    description='Tom hat uns sehr detaillierte Analytics-Berichte geliefert. Die Insights haben uns geholfen, bessere Entscheidungen zu treffen.'
)

review13 = Review.objects.create(
    business_user=profile1,
    reviewer=profile12,
    rating=5,
    description='Max hat eine atemberaubende Website für mein Startup erstellt. Die Kombination aus Design und Funktionalität ist perfekt.'
)


print("✅ Testdaten erfolgreich erstellt!")
print(f"📊 Erstellt: {User.objects.count()} Users, {Profile.objects.count()} Profiles, {Offer.objects.count()} Offers")
print(f"📊 Erstellt: {OfferDetail.objects.count()} OfferDetails, {Order.objects.count()} Orders, {Review.objects.count()} Reviews")
print(f"👥 Business Users: {Profile.objects.filter(type='business').count()}")
print(f"👤 Customer Users: {Profile.objects.filter(type='customer').count()}") 