QT += widgets
CONFIG += c++17

SOURCES += main.cpp \
           mainwindow.cpp

HEADERS += mainwindow.h

FORMS += mainwindow.ui

TRANSLATIONS += sih-intercom_en_IN.ts
CONFIG += embed_translations lrelease

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets
