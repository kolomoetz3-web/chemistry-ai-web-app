import re
import os
import pickle

# Проверяем доступность TensorFlow
try:
    import tensorflow as tf
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("⚠️ TensorFlow не установлен. Нейронная сеть будет недоступна.")
    print("Установите зависимости: pip install tensorflow numpy pandas scikit-learn")
    TENSORFLOW_AVAILABLE = False
    # Создаем заглушки для типов
    tf = None
    np = None
    pd = None
    train_test_split = None
    LabelEncoder = None

class NeuralChemistryPredictor:
    """Нейронная сеть для предсказания химических реакций"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_length = 50
        self.vocab_size = 1000
        self.model_path = 'neural_chemistry_model.h5'
        self.tokenizer_path = 'tokenizer.pkl'
        self.label_encoder_path = 'label_encoder.pkl'
        self.tensorflow_available = TENSORFLOW_AVAILABLE

    def create_training_data(self):
        """Создание обучающих данных на основе известных реакций"""
        reactions = [
            # Металл + кислота
            ("Li + HCl", "LiCl + H2"),
            ("Na + HCl", "NaCl + H2"),
            ("K + HCl", "KCl + H2"),
            ("Ca + HCl", "CaCl2 + H2"),
            ("Mg + HCl", "MgCl2 + H2"),
            ("Zn + HCl", "ZnCl2 + H2"),
            ("Fe + HCl", "FeCl2 + H2"),
            ("Al + HCl", "AlCl3 + H2"),

            # Металл + кислород
            ("Li + O2", "Li2O"),
            ("Na + O2", "Na2O"),
            ("K + O2", "K2O"),
            ("Ca + O2", "CaO"),
            ("Mg + O2", "MgO"),
            ("Zn + O2", "ZnO"),
            ("Fe + O2", "Fe2O3"),
            ("Al + O2", "Al2O3"),
            ("Cu + O2", "CuO"),

            # Кислота + основание
            ("HCl + NaOH", "NaCl + H2O"),
            ("H2SO4 + NaOH", "Na2SO4 + H2O"),
            ("HNO3 + NaOH", "NaNO3 + H2O"),
            ("HCl + KOH", "KCl + H2O"),
            ("H2SO4 + KOH", "K2SO4 + H2O"),
            ("HCl + Ca(OH)2", "CaCl2 + H2O"),

            # Горение
            ("C + O2", "CO2"),
            ("CH4 + O2", "CO2 + H2O"),
            ("C2H6 + O2", "CO2 + H2O"),
            ("C3H8 + O2", "CO2 + H2O"),
            ("H2 + O2", "H2O"),

            # Разложение
            ("CaCO3", "CaO + CO2"),
            ("Cu(OH)2", "CuO + H2O"),
            ("H2O2", "H2O + O2"),
            ("KClO3", "KCl + O2"),

            # Вытеснение
            ("Zn + CuSO4", "ZnSO4 + Cu"),
            ("Fe + CuSO4", "FeSO4 + Cu"),
            ("Al + CuSO4", "Al2(SO4)3 + Cu"),
        ]

        return reactions

    def tokenize_formula(self, formula):
        """Токенизация химической формулы"""
        # Разбиваем на элементы, числа и скобки
        tokens = re.findall(r'[A-Z][a-z]*|\d+|[()+\-\s]', formula)
        return ' '.join(tokens)

    def prepare_data(self, reactions):
        """Подготовка данных для обучения"""
        if not self.tensorflow_available:
            return None, None

        X_texts = []
        y_texts = []

        for reactants, products in reactions:
            # Токенизируем реагенты
            reactant_tokens = self.tokenize_formula(reactants)
            X_texts.append(reactant_tokens)

            # Токенизируем продукты
            product_tokens = self.tokenize_formula(products)
            y_texts.append(product_tokens)

        # Создаем токенизатор
        all_texts = X_texts + y_texts
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(
            num_words=self.vocab_size,
            oov_token='<OOV>'
        )
        self.tokenizer.fit_on_texts(all_texts)

        # Кодируем последовательности
        X_sequences = self.tokenizer.texts_to_sequences(X_texts)
        X_padded = tf.keras.preprocessing.sequence.pad_sequences(
            X_sequences, maxlen=self.max_length, padding='post'
        )

        # Для целевых данных используем one-hot encoding
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y_texts)
        y_categorical = tf.keras.utils.to_categorical(y_encoded)

        return X_padded, y_categorical

    def build_model(self):
        """Создание модели нейронной сети"""
        if not self.tensorflow_available or self.label_encoder is None:
            return None

        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(
                input_dim=self.vocab_size,
                output_dim=128,
                input_length=self.max_length
            ),
            tf.keras.layers.LSTM(128, return_sequences=True),
            tf.keras.layers.LSTM(64),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(len(self.label_encoder.classes_), activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        self.model = model
        return model

    def train(self, epochs=50, batch_size=16):
        """Обучение модели"""
        if not self.tensorflow_available:
            print("❌ TensorFlow недоступен. Обучение невозможно.")
            return None

        print("Создание обучающих данных...")
        reactions = self.create_training_data()
        X, y = self.prepare_data(reactions)

        print(f"Размер обучающего набора: {len(X)} примеров")

        # Разделяем на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print("Создание модели...")
        self.build_model()

        print("Обучение модели...")
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1
        )

        # Сохраняем модель и токенизаторы
        self.save_model()

        print("Обучение завершено!")
        return history

    def predict(self, reactants):
        """Предсказание продуктов реакции"""
        if not self.tensorflow_available:
            print("❌ TensorFlow недоступен. Используется правиловой подход.")
            return None

        if self.model is None:
            if not self.load_model():
                return None

        # Токенизируем входные данные
        reactant_tokens = self.tokenize_formula(reactants)
        sequence = self.tokenizer.texts_to_sequences([reactant_tokens])
        padded = tf.keras.preprocessing.sequence.pad_sequences(
            sequence, maxlen=self.max_length, padding='post'
        )

        # Предсказываем
        prediction = self.model.predict(padded, verbose=0)
        predicted_index = np.argmax(prediction[0])

        # Декодируем результат
        predicted_products = self.label_encoder.inverse_transform([predicted_index])[0]

        return predicted_products

    def save_model(self):
        """Сохранение модели и токенизаторов"""
        try:
            self.model.save(self.model_path)
            with open(self.tokenizer_path, 'wb') as f:
                pickle.dump(self.tokenizer, f)
            with open(self.label_encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            print("Модель сохранена успешно")
        except Exception as e:
            print(f"Ошибка сохранения модели: {e}")

    def load_model(self):
        """Загрузка модели и токенизаторов"""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                with open(self.tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                with open(self.label_encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print("Модель загружена успешно")
                return True
            else:
                print("Модель не найдена")
                return False
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            return False

    def get_model_info(self):
        """Получение информации о модели"""
        if not self.tensorflow_available:
            return """
❌ TensorFlow не установлен

🤖 Нейронная сеть недоступна

📦 Для активации ИИ установите зависимости:
pip install tensorflow numpy pandas scikit-learn

🔄 Пока работает правиловой алгоритм предсказания реакций
            """

        if self.model is None:
            return """
🤖 Нейронная сеть для предсказания реакций

📊 Статус: Модель не загружена
💡 Используйте /train для обучения модели

🔄 Сейчас работает правиловой алгоритм
            """

        info = f"""
🤖 Нейронная сеть для предсказания реакций

📊 Параметры модели:
• Размер словаря: {self.vocab_size}
• Максимальная длина последовательности: {self.max_length}
• Архитектура: LSTM (128 → 64)
• Активация: ReLU + Softmax

🎯 Точность: Модель обучена на {len(self.create_training_data())} примерах реакций
        """

        return info

# Функция для интеграции в существующий код
def predict_with_neural_network(reactants):
    """Функция для использования нейросети в боте"""
    predictor = NeuralChemistryPredictor()

    # Пытаемся загрузить существующую модель
    if not predictor.load_model():
        print("Модель не найдена, обучение новой модели...")
        predictor.train(epochs=30)
        print("Модель обучена!")

    prediction = predictor.predict(reactants)
    return prediction

if __name__ == "__main__":
    # Пример использования
    predictor = NeuralChemistryPredictor()

    if predictor.tensorflow_available:
        # Обучение модели
        print("🚀 Обучение нейронной сети...")
        predictor.train(epochs=30)

        # Тестирование
        test_reactions = ["Zn + HCl", "CH4 + O2", "Na + O2"]
        print("\n🧪 Тестирование предсказаний:")
        for reaction in test_reactions:
            prediction = predictor.predict(reaction)
            print(f"Вход: {reaction} → Предсказание: {prediction}")
    else:
        print("❌ TensorFlow недоступен.")
        print("Установите зависимости командой:")
        print("pip install tensorflow numpy pandas scikit-learn")
        print("\n🔄 Пока можно использовать правиловой алгоритм в боте.")