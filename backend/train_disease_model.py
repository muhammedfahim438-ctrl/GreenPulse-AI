# ══════════════════════════════
# GreenPulse AI — Train Disease
# Trains crop disease detection
# ══════════════════════════════

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


def create_training_data():
    np.random.seed(42)
    samples = 800

    healthy = np.column_stack([
        np.random.uniform(30,  80,  samples // 4),
        np.random.uniform(120, 200, samples // 4),
        np.random.uniform(30,  80,  samples // 4),
        np.random.uniform(0.1, 0.3, samples // 4),
        np.random.uniform(0.6, 0.9, samples // 4),
        np.random.uniform(0.05, 0.2, samples // 4)
    ])
    healthy_labels = np.zeros(samples // 4)

    blight = np.column_stack([
        np.random.uniform(100, 180, samples // 4),
        np.random.uniform(60,  120, samples // 4),
        np.random.uniform(20,  60,  samples // 4),
        np.random.uniform(0.4, 0.8, samples // 4),
        np.random.uniform(0.1, 0.4, samples // 4),
        np.random.uniform(0.3, 0.7, samples // 4)
    ])
    blight_labels = np.ones(samples // 4)

    rust = np.column_stack([
        np.random.uniform(150, 220, samples // 4),
        np.random.uniform(80,  140, samples // 4),
        np.random.uniform(10,  50,  samples // 4),
        np.random.uniform(0.5, 0.9, samples // 4),
        np.random.uniform(0.1, 0.3, samples // 4),
        np.random.uniform(0.4, 0.8, samples // 4)
    ])
    rust_labels = np.full(samples // 4, 2)

    mildew = np.column_stack([
        np.random.uniform(180, 240, samples // 4),
        np.random.uniform(180, 240, samples // 4),
        np.random.uniform(180, 240, samples // 4),
        np.random.uniform(0.1, 0.3, samples // 4),
        np.random.uniform(0.2, 0.4, samples // 4),
        np.random.uniform(0.3, 0.6, samples // 4)
    ])
    mildew_labels = np.full(samples // 4, 3)

    X = np.vstack([healthy, blight, rust, mildew])
    y = np.concatenate([
        healthy_labels,
        blight_labels,
        rust_labels,
        mildew_labels
    ])

    return X, y


def train():

    print('🔬 GreenPulse AI — Training Disease Detection Model...')
    print('=' * 55)

    X, y = create_training_data()
    print(f'✅ Created {len(X)} training samples')
    print(f'✅ Disease classes: 4')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print(f'✅ Training samples: {len(X_train)}')
    print(f'✅ Testing samples:  {len(X_test)}')

    print('\n🤖 Training disease classifier...')

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )

    model.fit(X_train, y_train)
    print('✅ Model trained successfully!')

    y_pred   = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print('\n📊 Model Performance:')
    print(f'   Accuracy: {round(accuracy * 100, 1)}%')

    print('\n📋 Classification Report:')
    print(classification_report(
        y_test, y_pred,
        target_names=[
            'Healthy',
            'Leaf Blight',
            'Rust Disease',
            'Powdery Mildew'
        ]
    ))

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/disease_model.pkl')
    print('✅ Model saved to models/disease_model.pkl')
    print('=' * 55)
    print('🎉 Disease Model Training Complete!')


if __name__ == '__main__':
    train()
