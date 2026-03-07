# ══════════════════════════════
# GreenPulse AI — Train Model
# Trains crop yield prediction
# using Scikit-learn
# ══════════════════════════════

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# ── create sample training data ──
# in real app you would use a real dataset
def create_training_data():

    np.random.seed(42)
    samples = 1000

    data = {
        # crop type as number
        # wheat=0 maize=1 rice=2 tomato=3 cotton=4 potato=5
        'crop': np.random.randint(0, 6, samples),

        # temperature between 10 and 45
        'temperature': np.random.uniform(10, 45, samples),

        # rainfall between 100 and 2500
        'rainfall': np.random.uniform(100, 2500, samples),

        # humidity between 20 and 95
        'humidity': np.random.uniform(20, 95, samples),

        # farm area between 1 and 50
        'area': np.random.uniform(1, 50, samples),

        # fertilizer level 0=none 1=low 2=medium 3=high
        'fertilizer': np.random.randint(0, 4, samples),

        # soil type 0=black 1=red 2=alluvial 3=sandy 4=clay
        'soil': np.random.randint(0, 5, samples),

        # season 0=kharif 1=rabi 2=zaid
        'season': np.random.randint(0, 3, samples),
    }

    df = pd.DataFrame(data)

    # ── calculate yield based on conditions ──
    base_yields = [3.2, 4.0, 2.5, 3.8, 1.8, 5.0]
    df['yield'] = df['crop'].apply(lambda x: base_yields[x])

    # temperature effect
    df.loc[df['temperature'] > 35, 'yield'] -= 0.5
    df.loc[df['temperature'] < 15, 'yield'] -= 0.4
    df.loc[
        (df['temperature'] >= 20) &
        (df['temperature'] <= 30), 'yield'
    ] += 0.3

    # rainfall effect
    df.loc[
        (df['rainfall'] >= 600) &
        (df['rainfall'] <= 1200), 'yield'
    ] += 0.3
    df.loc[df['rainfall'] < 300, 'yield'] -= 0.5
    df.loc[df['rainfall'] > 2000, 'yield'] -= 0.3

    # humidity effect
    df.loc[
        (df['humidity'] >= 50) &
        (df['humidity'] <= 80), 'yield'
    ] += 0.2
    df.loc[df['humidity'] > 90, 'yield'] -= 0.3

    # fertilizer effect
    df.loc[df['fertilizer'] == 3, 'yield'] += 0.4
    df.loc[df['fertilizer'] == 2, 'yield'] += 0.2
    df.loc[df['fertilizer'] == 0, 'yield'] -= 0.3

    # soil effect
    df.loc[df['soil'] == 2, 'yield'] += 0.2
    df.loc[df['soil'] == 3, 'yield'] -= 0.2

    # season effect
    df.loc[df['season'] == 1, 'yield'] += 0.1

    # add small random noise
    df['yield'] += np.random.uniform(-0.2, 0.2, samples)

    # make sure yield is never below 0.5
    df['yield'] = df['yield'].clip(lower=0.5)

    # round to 1 decimal
    df['yield'] = df['yield'].round(1)

    return df


def train():

    print('🌱 GreenPulse AI — Training Crop Yield Model...')
    print('=' * 50)

    # create training data
    df = create_training_data()
    print(f'✅ Created {len(df)} training samples')

    # separate features and target
    features = [
        'crop', 'temperature', 'rainfall',
        'humidity', 'area', 'fertilizer',
        'soil', 'season'
    ]

    X = df[features]
    y = df['yield']

    # split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print(f'✅ Training samples: {len(X_train)}')
    print(f'✅ Testing samples:  {len(X_test)}')

    # ── train Random Forest model ──
    print('\n🤖 Training Random Forest model...')

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )

    model.fit(X_train, y_train)
    print('✅ Model trained successfully!')

    # ── evaluate model ──
    y_pred = model.predict(X_test)
    mae    = mean_absolute_error(y_test, y_pred)
    r2     = r2_score(y_test, y_pred)

    print('\n📊 Model Performance:')
    print(f'   Mean Absolute Error : {mae:.3f}')
    print(f'   R2 Score            : {r2:.3f}')
    print(f'   Accuracy            : {round(r2 * 100, 1)}%')

    # ── save model to file ──
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/crop_yield_model.pkl')
    print('\n✅ Model saved to models/crop_yield_model.pkl')
    print('=' * 50)
    print('🎉 Training Complete!')


if __name__ == '__main__':
    train()