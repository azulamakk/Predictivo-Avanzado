from flask import Flask, request, jsonify, render_template
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import uuid

app = Flask(__name__)

# Cargar datos
df_ratings = pd.read_csv('./datos/rating_final.csv')
df_places = pd.read_csv('./datos/dataLocal.csv')
df_users = pd.read_csv('./datos/dataUser.csv')

# Configurar Surprise
reader = Reader(rating_scale=(0, 2))
data = Dataset.load_from_df(df_ratings[['userID', 'placeID', 'rating']], reader)

# Dividir datos para entrenamiento y prueba
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Configurar algoritmo KNN con MSD
algo = KNNBasic(k=20, sim_options={'name': 'msd', 'user_based': False})

# Entrenar el modelo
algo.fit(trainset)

# Función para recomendar lugares para un userID dado
def recommend_places(user_id, algo, df_places, top_n=10):
    recommendations = []

    # Obtener todos los IDs de lugar disponibles
    place_ids = df_places['placeID'].unique()

    # Predecir calificaciones para todos los lugares
    for place_id in place_ids:
        # Predecir la calificación para este lugar
        prediction = algo.predict(user_id, place_id)
        recommendations.append((place_id, prediction.est))

    # Ordenar recomendaciones por calificación estimada
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Obtener las mejores recomendaciones
    top_recommendations = recommendations[:top_n]

    # Preparar detalles de las mejores recomendaciones
    top_recommendations_details = []
    for place_id, rating in top_recommendations:
        place_info = df_places[df_places['placeID'] == place_id].iloc[0]
        top_recommendations_details.append({
            'Nombre': place_info['name'],
            'Dirección': place_info['address'],
            'Calificación Estimada': rating
        })

    return top_recommendations_details


# Ruta para ingresar datos de usuario y obtener recomendaciones
@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json

    # Generar un userID único para el nuevo usuario (U20 + 2 dígitos aleatorios)
    user_id = f"U20{uuid.uuid4().hex[:2].upper()}"

    global df_users  # Definir df_users como global para poder modificarlo dentro de la función

    # Agregar nuevo usuario a df_users
    new_user = pd.DataFrame([{'userID': user_id, 'latitude': None, 'longitude': None, **user_data}])
    df_users = pd.concat([df_users, new_user], ignore_index=True)
    # Guardar en CSV (opcional, si desea persistir los datos de nuevos usuarios)
    df_users.to_csv('./datos/dataUser.csv', index=False)

    # Obtener recomendaciones para el nuevo usuario
    recommendations = recommend_places(user_id, algo, df_places, df_ratings)

    return jsonify(recommendations)

# Ruta para la página de ingreso de datos
@app.route('/')
def index():
    # Valores únicos para dropdowns
    unique_budget = ['medium', 'low', '?', 'high']
    unique_interest = ['variety', 'technology', 'none', 'retro', 'eco-friendly']
    unique_personality = ['thrifty-protector', 'hunter-ostentatious', 'hard-worker', 'conformist']
    unique_religion = ['none', 'Catholic', 'Christian', 'Mormon', 'Jewish']
    unique_activity = ['student', 'professional', '?', 'unemployed', 'working-class']
    unique_smoker = ['false', 'true', '?']
    unique_drink_level = ['abstemious', 'social drinker', 'casual drinker']
    unique_dress_preference = ['informal', 'formal', 'no preference', '?', 'elegant']
    unique_ambience = ['family', 'friends', 'solitary', '?']
    unique_transport = ['on foot', 'public', 'car owner', '?']
    unique_marital_status = ['single', 'married', 'widow', '?']
    unique_hijos = ['independent', 'kids', '?', 'dependent']
    unique_Rcuisine = ['American', 'Mexican', 'Bakery', 'Family', 'Cafe-Coffee_Shop', 'Diner',
                       'Latin_American', 'Japanese', 'Chinese', 'Pizzeria', 'Afghan', 'Regional',
                       'Contemporary', 'Middle_Eastern', 'Bar', 'Breakfast-Brunch', 'Cuban',
                       'Burgers', 'Sushi', 'Italian', 'Tex-Mex', 'Game', 'Cafeteria', 'Barbecue',
                       'Turkish', 'Organic-Healthy']
    unique_Upayment = ['cash', 'MasterCard-Eurocard', 'bank_debit_cards', 'VISA', 'American_Express']

    return render_template('index.html', 
                           unique_budget=unique_budget,
                           unique_interest=unique_interest,
                           unique_personality=unique_personality,
                           unique_religion=unique_religion,
                           unique_activity=unique_activity,
                           unique_smoker=unique_smoker,
                           unique_drink_level=unique_drink_level,
                           unique_dress_preference=unique_dress_preference,
                           unique_ambience=unique_ambience,
                           unique_transport=unique_transport,
                           unique_marital_status=unique_marital_status,
                           unique_hijos=unique_hijos,
                           unique_Rcuisine=unique_Rcuisine,
                           unique_Upayment=unique_Upayment)

if __name__ == '__main__':
    app.run(debug=True)
