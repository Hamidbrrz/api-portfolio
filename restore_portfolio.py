import requests

BASE_URL = "https://api-portfolio-1-puyb.onrender.com/api"

# === À PROPOS ===
about_data = {
    "name": "Hamid Brz",
    "title": "Développeur Web & Mobile | React · Next.js · Flask",
    "bio": "Passionné par la technologie et le design, je crée des expériences modernes avec React, Next.js et Flask. Mon objectif ? Allier performance, design et simplicité pour des projets qui ont de l’impact. Toujours curieux, je me forme chaque jour pour maîtriser les outils d’aujourd’hui et anticiper ceux de demain.",
    "image_url": "/hamid.jpg"
}
requests.post(f"{BASE_URL}/about", json=about_data)


# === PROJETS ===
projects = [
    {
        "title": "DevPortfolio",
        "description": "Un portfolio moderne construit avec Next.js, Tailwind CSS et une API Flask pour gérer dynamiquement les projets, le blog et le contact. Design minimaliste et 100% responsive.",
        "link": "https://web-portfolio-blush.vercel.app/"
    },
    {
        "title": "CondoQClean",
        "description": "Application web pour réserver un service de lavage express pour condos au Québec. Interface fluide, formulaire de réservation, et panneau admin intégré. Stack : React · Flask · Vercel.",
        "link": "https://condoqclean.com"
    },
    {
        "title": "TaskSprint",
        "description": "App de gestion de tâches rapide et élégante, conçue avec React Native et Flask. Permet de créer, modifier et suivre l'avancement de tâches en temps réel.",
        "link": "https://tasksprint-demo.vercel.app"
    }
]
for p in projects:
    requests.post(f"{BASE_URL}/projects", json=p)


# === BLOG ===
blog_articles = [
    {
        "title": "Une version mobile arrive dans les prochains jours",
        "content": "Je travaille actuellement sur une version mobile de mon portfolio avec React Native et Expo. Elle permettra de découvrir mes projets directement depuis un téléphone, avec une interface fluide et rapide. Disponible très bientôt !"
    },
    {
        "title": "J’espère que Steve appréciera mon travail",
        "content": "Ce portfolio est un projet personnel que j’ai conçu avec passion. J’ai tout fait moi-même, du backend Flask à l’interface Next.js, en passant par l’admin. C’est aussi un défi pour impressionner Steve et lui montrer mes compétences 💪"
    },
    {
        "title": "3 nuits, 0 excuses",
        "content": "J’ai réalisé ce projet en seulement trois nuits. La semaine était très chargée avec le travail, mais je voulais absolument terminer ce portfolio dans les temps. Le résultat : une plateforme complète, fonctionnelle, et déployée sur Vercel."
    },
    {
        "title": "Je vais retravailler l’UI/UX et le responsive design",
        "content": "Le projet fonctionne, mais je prévois bientôt d’améliorer encore plus le design, l’ergonomie et le responsive. Objectif : proposer une expérience plus fluide, plus claire et plus agréable sur tous les écrans."
    }
]
for article in blog_articles:
    requests.post(f"{BASE_URL}/blog", json=article)


# === CONTACT ===
contact_data = {
    "email": "brrzhamid@gmail.com",
    "linkedin": "https://www.linkedin.com/in/ahmed-abdelhamid-berrazouane-62aa43247/?originalSubdomain=ca",
    "github": "https://github.com/Hamidbrrz",
    "message": "Merci de visiter mon portfolio ! N’hésitez pas à me contacter pour collaborer ou échanger 🔥"
}
requests.post(f"{BASE_URL}/contact", json=contact_data)

print("✅ Données restaurées avec succès !")
