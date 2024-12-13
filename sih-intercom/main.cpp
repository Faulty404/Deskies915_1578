#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QMessageBox>
#include <QWidget>
#include <QSplitter>
#include <QColorDialog>
#include <QTextEdit>
#include <QSlider>
#include <QLineEdit>
#include <QHBoxLayout>

class VideoCallApp : public QMainWindow {
    Q_OBJECT

public:
    VideoCallApp(QWidget *parent = nullptr) : QMainWindow(parent) {
        // Main widget and layout
        QWidget *centralWidget = new QWidget(this);
        mainLayout = new QVBoxLayout(centralWidget);

        // Title label
        titleLabel = new QLabel("Video Call Application", this);
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("font-size: 18px; font-weight: bold;");
        mainLayout->addWidget(titleLabel);

        // Question section
        questionLabel = new QLabel("Are you deaf?", this);
        questionLabel->setAlignment(Qt::AlignCenter);
        questionLabel->setStyleSheet("font-size: 16px;");
        mainLayout->addWidget(questionLabel);

        yesButton = new QPushButton("Yes", this);
        noButton = new QPushButton("No", this);

        connect(yesButton, &QPushButton::clicked, this, &VideoCallApp::handleYes);
        connect(noButton, &QPushButton::clicked, this, &VideoCallApp::handleNo);

        QHBoxLayout *buttonLayout = new QHBoxLayout;
        buttonLayout->addWidget(yesButton);
        buttonLayout->addWidget(noButton);
        mainLayout->addLayout(buttonLayout);

        // Color change button
        colorButton = new QPushButton("Change Colors", this);
        connect(colorButton, &QPushButton::clicked, this, &VideoCallApp::openColorDialog);
        mainLayout->addWidget(colorButton);

        // Caption size adjustment (slider)
        captionSizeSlider = new QSlider(Qt::Horizontal, this);
        captionSizeSlider->setRange(50, 200); // 50% to 200%
        captionSizeSlider->setValue(100); // Default size is 100%
        connect(captionSizeSlider, &QSlider::valueChanged, this, &VideoCallApp::adjustCaptionSize);

        captionSizeLabel = new QLabel("Caption Size: 100%", this);
        QHBoxLayout *captionSizeLayout = new QHBoxLayout;
        captionSizeLayout->addWidget(captionSizeLabel);
        captionSizeLayout->addWidget(captionSizeSlider);
        mainLayout->addLayout(captionSizeLayout);

        // Video call section placeholder (initially hidden)
        videoContainer = new QSplitter(Qt::Vertical, this);
        videoContainer->setVisible(false);
        mainLayout->addWidget(videoContainer);

        setCentralWidget(centralWidget);
        setWindowTitle("Video Call App");
        resize(400, 300);
    }

private slots:
    void handleYes() {
        QMessageBox::information(this, "Interpreter Added", "An interpreter has been added to the call.");
        setupVideoCallLayout(true);
    }

    void handleNo() {
        QMessageBox::information(this, "Response Recorded", "No interpreter needed.");
        setupVideoCallLayout(false);
    }

    void openColorDialog() {
        QColorDialog *colorDialog = new QColorDialog(this);
        QColor selectedColor = colorDialog->getColor(Qt::white, this, "Select Background Color");

        if (selectedColor.isValid()) {
            QString colorStyle = QString("background-color: %1;").arg(selectedColor.name());
            this->setStyleSheet(colorStyle);
        }
    }

    void adjustCaptionSize(int value) {
        // Adjust the caption size based on the slider value (percentage)
        int fontSize = value; // The slider value will be the percentage of the default font size
        captionLabel->setStyleSheet(QString("font-size: %1px;").arg(fontSize));
        captionSizeLabel->setText(QString("Caption Size: %1%").arg(value));
    }

    void sendMessage() {
        QString message = chatInputField->text();
        if (!message.isEmpty()) {
            // Display the message in the chat area
            chatDisplay->append(QString("<b>You:</b> %1").arg(message));
            chatInputField->clear(); // Clear the input field
        }
    }

    void toggleCaptions() {
        if (captionsEnabled) {
            // Switch to sign language captions
            captionLabel->setText("Sign Language Captions: [Sign language animation here]");
            captionsButton->setText("Enable Speech-to-Text Captions");
        } else {
            // Switch to speech-to-text captions
            captionLabel->setText("Speech-to-Text Captions: [Live speech-to-text here]");
            captionsButton->setText("Enable Sign Language Captions");
        }

        captionsEnabled = !captionsEnabled;
    }

    void enableCaptionsAfterCall() {
        // Enable the captions button after the video call begins
        captionsButton = new QPushButton("Enable Captions", this);
        connect(captionsButton, &QPushButton::clicked, this, &VideoCallApp::toggleCaptions);
        mainLayout->addWidget(captionsButton);
    }

private:
    QLabel *titleLabel;
    QLabel *questionLabel;
    QPushButton *yesButton;
    QPushButton *noButton;
    QPushButton *colorButton;
    QPushButton *captionsButton;
    QSplitter *videoContainer;
    QVBoxLayout *mainLayout;
    QLabel *captionLabel;
    QLabel *captionSizeLabel;
    QSlider *captionSizeSlider;

    QLineEdit *chatInputField;
    QTextEdit *chatDisplay;
    QPushButton *sendButton;

    bool captionsEnabled = false;

    void setupVideoCallLayout(bool withInterpreter) {
        // Hide the question and buttons
        titleLabel->setVisible(false);
        questionLabel->setVisible(false);
        yesButton->setVisible(false);
        noButton->setVisible(false);
        colorButton->setVisible(false); // Hide the color change button during the call

        // Show the video container
        videoContainer->setVisible(true);

        // Clear previous widgets if any
        for (auto widget : videoContainer->findChildren<QWidget *>()) {
            delete widget;
        }

        // Create video blocks
        if (withInterpreter) {
            // Display interpreter along with two participants
            QLabel *interpreterVideo = new QLabel("[Interpreter Video]");
            interpreterVideo->setStyleSheet("border: 1px solid black; background: lightgray;");
            interpreterVideo->setAlignment(Qt::AlignCenter);

            QSplitter *participantsSplitter = new QSplitter(Qt::Horizontal, this);
            QLabel *personA = new QLabel("[Person A Video]");
            personA->setStyleSheet("border: 1px solid black; background: lightgray;");
            personA->setAlignment(Qt::AlignCenter);

            QLabel *personB = new QLabel("[Person B Video]");
            personB->setStyleSheet("border: 1px solid black; background: lightgray;");
            personB->setAlignment(Qt::AlignCenter);

            participantsSplitter->addWidget(personA);
            participantsSplitter->addWidget(personB);

            videoContainer->addWidget(interpreterVideo);
            videoContainer->addWidget(participantsSplitter);

            // Adjustable proportions
            videoContainer->setStretchFactor(0, 3); // Interpreter video gets more space
            videoContainer->setStretchFactor(1, 1); // Participants section gets less space
            participantsSplitter->setStretchFactor(0, 1); // Calling person's video smaller
            participantsSplitter->setStretchFactor(1, 2); // Other person's video larger
        } else {
            // Display only the two participants without interpreter
            QSplitter *participantsSplitter = new QSplitter(Qt::Horizontal, this);
            QLabel *personA = new QLabel("[Person A Video]");
            personA->setStyleSheet("border: 1px solid black; background: lightgray;");
            personA->setAlignment(Qt::AlignCenter);

            QLabel *personB = new QLabel("[Person B Video]");
            personB->setStyleSheet("border: 1px solid black; background: lightgray;");
            personB->setAlignment(Qt::AlignCenter);

            participantsSplitter->addWidget(personA);
            participantsSplitter->addWidget(personB);

            videoContainer->addWidget(participantsSplitter);

            // Adjustable proportions for the two participants
            participantsSplitter->setStretchFactor(0, 1); // Calling person's video smaller
            participantsSplitter->setStretchFactor(1, 2); // Other person's video larger
        }

        // Caption display (Initially no captions)
        captionLabel = new QLabel("Captions will appear here", this);
        captionLabel->setAlignment(Qt::AlignCenter);
        captionLabel->setStyleSheet("font-size: 14px; font-weight: bold; color: black;");
        videoContainer->addWidget(captionLabel);

        // Create chat interface
        chatDisplay = new QTextEdit(this);
        chatDisplay->setReadOnly(true);  // Make the chat display read-only
        chatDisplay->setStyleSheet("border: 1px solid black; background: lightgray;");
        videoContainer->addWidget(chatDisplay);

        // Chat input field
        chatInputField = new QLineEdit(this);
        chatInputField->setPlaceholderText("Type a message...");
        videoContainer->addWidget(chatInputField);

        // Send button for chat
        sendButton = new QPushButton("Send", this);
        connect(sendButton, &QPushButton::clicked, this, &VideoCallApp::sendMessage);
        videoContainer->addWidget(sendButton);

        // Enable captions after the video call starts
        enableCaptionsAfterCall();
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    VideoCallApp mainWindow;
    mainWindow.show();

    return app.exec();
}

#include "main.moc"
