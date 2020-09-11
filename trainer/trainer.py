from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from utils.utils import  configInfo
from sklearn.metrics import classification_report

class Trainer:
    def __init__(self, dataloader, model, config, INIT_LR=1e-4, BATCH_SIZE=8, EPOCHS=50):

        self.dataloader = dataloader
        self.model = model
        self.config = configInfo(config)
        self.lr = INIT_LR
        self.BS = BATCH_SIZE
        self.EPOCHS = EPOCHS
        self.aug = ImageDataGenerator(rotation_range=20, zoom_range=0.15,
                                 width_shift_range=0.2, height_shift_range=0.2, shear_range=0.15,
                                 horizontal_flip=True, fill_mode="nearest")
        self.saved_model = self.config["saved_model"]
        self.saved_le = self.config["saved_le"]
        self.leclasses = dataloader.leclasses



    def train(self):

        trainX, testX, trainY, testY = self.dataloader.split()
        opt = Adam(lr=self.lr, decay=self.lr / self.EPOCHS)
        # model = LivenessNet.build(width=32, height=32, depth=3, classes=2)
        self.model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

        # 딥러닝 학습
        print("[INFO] training network for {} epochs...".format(self.EPOCHS))
        H = self.model.fit(self.aug.flow(trainX, trainY, batch_size=self.BS),
                                     validation_data=(testX, testY), steps_per_epoch=len(trainX) // self.BS,
                                     epochs=self.EPOCHS)

        print(f"[INFO] serializing network to '{self.saved_model}'...")
        self.model.save(self.saved_model)

        print("[INFO] evaluating network...")
        predictions = self.model.predict(testX, batch_size=self.BS)
        print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1), target_names=self.dataloader.leclasses))

        return H


