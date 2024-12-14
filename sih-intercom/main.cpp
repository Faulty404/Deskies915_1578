#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QMessageBox>
#include <QWidget>
#include <QSplitter>
#include <QColorDialog>
#include <QSpacerItem>
#include <QHBoxLayout>

class VideoCallApp : public QMainWindow {
    Q_OBJECT

public:
    VideoCallApp(QWidget *parent = nullptr) : QMainWindow(parent) {
        // Main widget and layout
        centralWidget = new QWidget(this);
        mainLayout = new QVBoxLayout(centralWidget);

        // Title label
        titleLabel = new QLabel("Signa Intercom", this);
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("font-size: 20px; font-weight: bold;");
        mainLayout->addWidget(titleLabel);

        // Spacer to separate title from question
        mainLayout->addSpacerItem(new QSpacerItem(0, 20));

        // Question section inside rectangular box
        questionContainer = new QWidget(this);
        QVBoxLayout *questionLayout = new QVBoxLayout(questionContainer);
        questionLabel = new QLabel("Are you deaf?", this);
        questionLabel->setAlignment(Qt::AlignCenter);
        questionLabel->setStyleSheet("font-size: 16px;");
        questionContainer->setStyleSheet(
            "border: 2px solid black; border-radius: 5px; padding: 10px;"
            );
        questionLayout->addWidget(questionLabel);

        yesButton = new QPushButton("Yes", this);
        noButton = new QPushButton("No", this);

        connect(yesButton, &QPushButton::clicked, this, &VideoCallApp::handleYes);
        connect(noButton, &QPushButton::clicked, this, &VideoCallApp::handleNo);

        QHBoxLayout *buttonLayout = new QHBoxLayout;
        buttonLayout->addWidget(yesButton);
        buttonLayout->addWidget(noButton);
        questionLayout->addLayout(buttonLayout);

        mainLayout->addWidget(questionContainer);

        // Spacer to separate question section and footer
        mainLayout->addSpacerItem(new QSpacerItem(0, 20));

        // Color change button at the bottom
        colorButton = new QPushButton("Change Colors", this);
        connect(colorButton, &QPushButton::clicked, this, &VideoCallApp::openColorDialog);
        mainLayout->addWidget(colorButton);

        // Set up notifications button at the bottom left corner
        notificationsButton = new QPushButton("🔔", this);
        notificationsButton->setFixedSize(50, 50); // Set size for circular button
        notificationsButton->setStyleSheet(
            "border-radius: 25px; "
            "background-color: #007BFF; "
            "color: white; "
            "font-size: 18px;"
            );
        bottomLayout = new QHBoxLayout();
        bottomLayout->addWidget(notificationsButton, 0, Qt::AlignLeft);
        bottomLayout->addStretch();
        mainLayout->addLayout(bottomLayout);

        connect(notificationsButton, &QPushButton::clicked, this, &VideoCallApp::showNotificationsMenu);

        setCentralWidget(centralWidget);
        setWindowTitle("Signa Intercom");
        resize(400, 500);
    }

private slots:
    void showNotificationsMenu() {
        QMessageBox msgBox(this);
        msgBox.setWindowTitle("Notifications");
        msgBox.setText("Choose an action:");

        QPushButton *emergencyMeetingButton = msgBox.addButton("Emergency Meeting", QMessageBox::ActionRole);
        QPushButton *routineReminderButton = msgBox.addButton("Routine Reminder", QMessageBox::ActionRole);
        QPushButton *cancelButton = msgBox.addButton("Cancel", QMessageBox::RejectRole);

        msgBox.exec();

        if (msgBox.clickedButton() == emergencyMeetingButton) {
            QMessageBox::information(this, "Emergency Meeting", "Emergency meeting has been scheduled.");
        } else if (msgBox.clickedButton() == routineReminderButton) {
            QMessageBox::information(this, "Routine Reminder", "Routine reminder has been set.");
        } else if (msgBox.clickedButton() == cancelButton) {
            QMessageBox::information(this, "Cancelled", "Action cancelled.");
        }
    }

    void handleYes() {
        setupVideoCallInterface(true);
    }

    void handleNo() {
        setupVideoCallInterface(false);
    }

    void openColorDialog() {
        QColorDialog *colorDialog = new QColorDialog(this);
        QColor selectedColor = colorDialog->getColor(Qt::white, this, "Select Background Color");

        if (selectedColor.isValid()) {
            QString colorStyle = QString("background-color: %1;").arg(selectedColor.name());
            this->setStyleSheet(colorStyle);
        }
    }

    void setupVideoCallInterface(bool withInterpreter) {
        // Hide the initial UI
        questionContainer->setVisible(false);
        titleLabel->setVisible(false);
        notificationsButton->setVisible(false);
        colorButton->setVisible(false);

        // Set up the new main video call interface
        QWidget *videoInterfaceContainer = new QWidget(this);
        QVBoxLayout *videoLayout = new QVBoxLayout(videoInterfaceContainer);

        if (withInterpreter) {
            // Interpreter + Two participants
            QSplitter *mainSplitter = new QSplitter(Qt::Horizontal, this);

            QLabel *interpreterVideo = new QLabel("[Interpreter Video]");
            interpreterVideo->setStyleSheet("border: 2px solid black; background: lightblue;");
            interpreterVideo->setAlignment(Qt::AlignCenter);

            QSplitter *participantsSplitter = new QSplitter(Qt::Vertical, this);
            QLabel *personAVideo = new QLabel("[Person A Video]");
            QLabel *personBVideo = new QLabel("[Person B Video]");

            personAVideo->setStyleSheet("border: 2px solid black; background: lightgray;");
            personBVideo->setStyleSheet("border: 2px solid black; background: lightgray;");

            participantsSplitter->addWidget(personAVideo);
            participantsSplitter->addWidget(personBVideo);

            mainSplitter->addWidget(interpreterVideo);
            mainSplitter->addWidget(participantsSplitter);

            mainSplitter->setStretchFactor(0, 3);
            mainSplitter->setStretchFactor(1, 1);

            videoLayout->addWidget(mainSplitter);
        } else {
            // Two participants only
            QSplitter *participantsSplitter = new QSplitter(Qt::Horizontal, this);
            QLabel *personAVideo = new QLabel("[Person A Video]");
            QLabel *personBVideo = new QLabel("[Person B Video]");

            personAVideo->setStyleSheet("border: 2px solid black; background: lightgray;");
            personBVideo->setStyleSheet("border: 2px solid black; background: lightgray;");

            participantsSplitter->addWidget(personAVideo);
            participantsSplitter->addWidget(personBVideo);

            participantsSplitter->setStretchFactor(0, 1);
            participantsSplitter->setStretchFactor(1, 1);

            videoLayout->addWidget(participantsSplitter);
        }

        // Add End Call Button
        QPushButton *endCallButton = new QPushButton("End Call", this);
        connect(endCallButton, &QPushButton::clicked, this, &VideoCallApp::resetToInitialState);
        videoLayout->addWidget(endCallButton);

        setCentralWidget(videoInterfaceContainer);
    }

    void resetToInitialState() {
        setCentralWidget(centralWidget);

        questionContainer->setVisible(true);
        titleLabel->setVisible(true);
        notificationsButton->setVisible(true);
        colorButton->setVisible(true);
    }

private:
    QPushButton *notificationsButton;
    QLabel *questionLabel;
    QPushButton *yesButton, *noButton, *colorButton;
    QWidget *questionContainer;
    QVBoxLayout *mainLayout;
    QHBoxLayout *bottomLayout;
    QWidget *centralWidget;
    QLabel *titleLabel;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    VideoCallApp mainWindow;
    mainWindow.show();

    return app.exec();
}

#include "main.moc"
