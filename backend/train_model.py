# ══════════════════════════════
# GreenPulse AI — Train Model
# Improved version with 15 crops
# ══════════════════════════════

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os


def create_training_data():

    np.random.seed(42)
    samples = 3000

    # 15 crops now!
    crop_yields = {
        0:  ('wheat',      3.2),
        1:  ('maize',      4.0),
        2:  ('rice',       2.5),
        3:  ('tomato',     3.8),
        4:  ('cotton',     1.8),
        5:  ('potato',     5.0),
        6:  ('sugarcane',  6.5),
        7:  ('soybean',    2.8),
        8:  ('sunflower',  2.2),
        9:  ('groundnut',  2.0),
        10: ('onion',      4.5),
        11: ('banana',     3.5),
        12: ('mango',      2.8),
        13: ('chilli',     1.5),
        14: ('turmeric',   2.3)
    }

    data = {
        'crop':        np.random.randint(0, 15, samples),
        'temperature': np.random.uniform(10, 45, samples),
        'rainfall':    np.random.uniform(100, 2500, samples),
        'humidity':    np.random.uniform(20, 95, samples),
        'area':        np.random.uniform(1, 50, samples),
        'fertilizer':  np.random.randint(0, 4, samples),
        'soil':        np.random.randint(0, 5, samples),
        'season':      np.random.randint(0, 3, samples),
        'ph_level':    np.random.uniform(4.5, 8.5, samples),
        'irrigation':  np.random.randint(0, 3, samples),
    }

    df = pd.DataFrame(data)

    # base yield per crop
    df['yield'] = df['crop'].apply(
        lambda x: crop_yields[x][1]
    )

    # temperature effect
    df.loc[df['temperature'] > 38, 'yield'] -= 0.8
    df.loc[df['temperature'] > 35, 'yield'] -= 0.5
    df.loc[df['temperature'] < 12, 'yield'] -= 0.6
    df.loc[df['temperature'] < 15, 'yield'] -= 0.4
    df.loc[
        (df['temperature'] >= 20) &
        (df['temperature'] <= 30), 'yield'
    ] += 0.5

    # rainfall effect
    df.loc[
        (df['rainfall'] >= 600) &
        (df['rainfall'] <= 1200), 'yield'
    ] += 0.5
    df.loc[df['rainfall'] < 200, 'yield'] -= 0.8
    df.loc[df['rainfall'] < 300, 'yield'] -= 0.5
    df.loc[df['rainfall'] > 2000, 'yield'] -= 0.4

    # humidity effect
    df.loc[
        (df['humidity'] >= 50) &
        (df['humidity'] <= 80), 'yield'
    ] += 0.3
    df.loc[df['humidity'] > 90, 'yield'] -= 0.4
    df.loc[df['humidity'] < 30, 'yield'] -= 0.3

    # fertilizer effect
    df.loc[df['fertilizer'] == 3, 'yield'] += 0.6
    df.loc[df['fertilizer'] == 2, 'yield'] += 0.3
    df.loc[df['fertilizer'] == 1, 'yield'] += 0.1
    df.loc[df['fertilizer'] == 0, 'yield'] -= 0.5

    # soil effect
    df.loc[df['soil'] == 2, 'yield'] += 0.3  # alluvial best
    df.loc[df['soil'] == 0, 'yield'] += 0.2  # black good
    df.loc[df['soil'] == 3, 'yield'] -= 0.3  # sandy bad

    # season effect
    df.loc[df['season'] == 1, 'yield'] += 0.2  # rabi best
    df.loc[df['season'] == 0, 'yield'] += 0.1  # kharif good

    # ph level effect
    df.loc[
        (df['ph_level'] >= 6.0) &
        (df['ph_level'] <= 7.5), 'yield'
    ] += 0.3
    df.loc[df['ph_level'] < 5.5, 'yield'] -= 0.4
    df.loc[df['ph_level'] > 8.0, 'yield'] -= 0.3

    # irrigation effect
    df.loc[df['irrigation'] == 2, 'yield'] += 0.4  # drip best
    df.loc[df['irrigation'] == 1, 'yield'] += 0.2  # sprinkler
    df.loc[df['irrigation'] == 0, 'yield'] -= 0.2  # rainfed

    # add noise
    df['yield'] += np.random.uniform(-0.15, 0.15, samples)
    df['yield']  = df['yield'].clip(lower=0.5)
    df['yield']  = df['yield'].round(2)

    return df


def train():

    print('🌱 GreenPulse AI — Training Improved Crop Yield Model...')
    print('=' * 55)

    df = create_training_data()
    print(f'✅ Created {len(df)} training samples')
    print(f'✅ Crops supported: 15')

    features = [
        'crop', 'temperature', 'rainfall',
        'humidity', 'area', 'fertilizer',
        'soil', 'season', 'ph_level', 'irrigation'
    ]

    X = df[features]
    y = df['yield']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print(f'✅ Training samples: {len(X_train)}')
    print(f'✅ Testing samples:  {len(X_test)}')

    # use Gradient Boosting for better accuracy
    print('\n🤖 Training Gradient Boosting model...')

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)
    print('✅ Model trained successfully!')

    y_pred = model.predict(X_test)
    mae    = mean_absolute_error(y_test, y_pred)
    r2     = r2_score(y_test, y_pred)

    print('\n📊 Model Performance:')
    print(f'   Mean Absolute Error : {mae:.3f}')
    print(f'   R2 Score            : {r2:.3f}')
    print(f'   Accuracy            : {round(r2 * 100, 1)}%')

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/crop_yield_model.pkl')

    # save feature names
    joblib.dump(features, 'models/feature_names.pkl')

    print('\n✅ Model saved to models/crop_yield_model.pkl')
    print('=' * 55)
    print('🎉 Training Complete!')


if __name__ == '__main__':
    train()