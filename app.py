# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
import threading
from utils.eleven_labs import generate_voice_reminder, create_reminder_message

# Charger les variables d'environnement
load_dotenv()

# Configuration de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialiser l'application Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")

# Page d'accueil publique
@app.route('/')
def index():
    return render_template('index.html')

# Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            if response.session:
                session['user_id'] = response.user.id
                session['user'] = {
                    'first_name': response.user.user_metadata.get('first_name', 'Utilisateur'),
                    'last_name': response.user.user_metadata.get('last_name', ''),
                    'email': response.user.email
                }
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Email ou mot de passe incorrect")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return render_template('login.html', error="Erreur lors de la connexion")
    return render_template('login.html')

# Page d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            
            if request.form['password'] != request.form['confirm_password']:
                return render_template('register.html', error="Les mots de passe ne correspondent pas")
            
            response = supabase.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {
                        'first_name': first_name,
                        'last_name': last_name
                    }
                }
            })
            if response.user:
                session['user_id'] = response.user.id
                session['user'] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                }
                return redirect(url_for('dashboard'))
            else:
                return render_template('register.html', error="Erreur lors de l'inscription")
        except Exception as e:
            print(f"Erreur d'inscription : {e}")
            return render_template('register.html', error="Erreur lors de l'inscription")
    return render_template('register.html')

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    supabase.auth.sign_out()
    return redirect(url_for('index'))

# Tableau de bord
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        response = supabase.table('rendezvous').select('*').eq('user_id', session['user_id']).execute()
        rendez_vous = response.data or []
        tasks = [
            {'title': 'Finaliser le rapport trimestriel', 'due_date': '2025-06-20', 'priority': 'high', 'completed': False},
            {'title': 'Envoyer les propositions clients', 'due_date': '2025-06-21', 'priority': 'medium', 'completed': False},
            {'title': 'Répondre aux emails', 'due_date': '2025-06-19', 'priority': 'low', 'completed': True},
            {'title': 'Préparer la présentation', 'due_date': '2025-06-20', 'priority': 'low', 'completed': False}
        ]
        return render_template('dashboard.html', rendez_vous=rendez_vous, tasks=tasks, user=session['user'])
    except Exception as e:
        print(f"Erreur lors du chargement du tableau de bord : {e}")
        return redirect(url_for('login'))

# Route pour ajouter un rendez-vous
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_rdv():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            titre = request.form['titre']
            date = request.form['date']
            heure = request.form['heure']
            description = request.form['description']
            
            supabase.table('rendezvous').insert({
                'user_id': session['user_id'],
                'titre': titre,
                'date': date,
                'heure': heure,
                'description': description
            }).execute()
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Erreur lors de l'ajout du rendez-vous : {e}")
            return render_template('ajouter_rdv.html', error="Erreur lors de l'ajout", user=session['user'])
    return render_template('ajouter_rdv.html', user=session['user'])

# Route pour modifier ou supprimer un rendez-vous
@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_rdv(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            if 'supprimer' in request.form:
                supabase.table('rendezvous').delete().eq('id', id).eq('user_id', session['user_id']).execute()
            else:
                titre = request.form['titre']
                date = request.form['date']
                heure = request.form['heure']
                description = request.form['description']
                supabase.table('rendezvous').update({
                    'titre': titre,
                    'date': date,
                    'heure': heure,
                    'description': description
                }).eq('id', id).eq('user_id', session['user_id']).execute()
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Erreur lors de la modification/suppression : {e}")
            return render_template('modifier_rdv.html', rdv={}, error="Erreur lors de l'opération", user=session['user'])
    
    try:
        response = supabase.table('rendezvous').select('*').eq('id', id).eq('user_id', session['user_id']).execute()
        if response.data:
            rdv = response.data[0]
            return render_template('modifier_rdv.html', rdv=rdv, user=session['user'])
        else:
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Erreur lors de la récupération du rendez-vous : {e}")
        return redirect(url_for('dashboard'))

# Route API pour les notifications
@app.route('/api/rendezvous')
def api_rendezvous():
    if 'user_id' not in session:
        return jsonify([]), 401
    
    try:
        response = supabase.table('rendezvous').select('*').eq('user_id', session['user_id']).execute()
        return jsonify(response.data or [])
    except Exception as e:
        print(f"Erreur API : {e}")
        return jsonify([]), 500

# Fonction pour vérifier et envoyer des rappels vocaux
def check_and_send_reminders():
    try:
        response = supabase.table('rendezvous').select('*').execute()
        rendezvous = response.data or []
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')

        for rdv in rendezvous:
            if rdv['date'] == tomorrow_str:
                message = create_reminder_message(rdv)
                audio_path = generate_voice_reminder(message)
                print(f"Rappel vocal généré pour {rdv['titre']} : {audio_path}")
                # Enregistrer le rappel pour l'affichage
                supabase.table('rappels').insert({
                    'user_id': rdv['user_id'],
                    'rdv_id': rdv['id'],
                    'audio_path': audio_path,
                    'created_at': datetime.now().isoformat()
                }).execute()
    except Exception as e:
        print(f"Erreur lors de la génération des rappels : {e}")

# Planifier les rappels vocaux tous les jours à 18h00
schedule.every().day.at("18:00").do(check_and_send_reminders)

# Fonction pour exécuter le planificateur dans un thread séparé
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Lancer l'application
if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(debug=True)