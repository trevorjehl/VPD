// Import the standard GUI elements from QTQuick
import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.2

// Import the Uranium GUI elements, which are themed for Cura
import UM 1.1 as UM
import Cura 1.0 as Cura

// Dialog
Window
{
    id: base

    property variant catalog: UM.I18nCatalog { name: "calibration" }
	
    title: catalog.i18nc("@title", "Calibration Shapes")

    color: "#fafafa" //Background color of cura: #fafafa

    // NonModal like that the dialog to block input in the main window
    modality: Qt.NonModal

    // WindowStaysOnTopHint to stay on top
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint

    // Setting the dimensions of the dialog window
    width: 250
    height: 50
    minimumWidth: 250
    minimumHeight: 50

    // Position of the window
    x: Screen.width*0.5 - width - 50
    y: 400 

    // Define a Window a border (Red for) and a background color
    Rectangle {
        id: bg_rect
        width: 250
        height: 50
        color: "#fff"
        border.color: "#D22"
        border.width: 3
        radius: 4
    }

    // Connecting our variable to the computed property of the manager
    property string userInfoText: manager.userInfoText
	
	property string sizeInput: manager.sizeInput

    // Button for closing the dialogbox
    Button
    {
        id: close_button
        text: "<font color='#ffffff'>" + "x" + "</font>"
        width: 25
        height: 25

        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.right: parent.right
        anchors.rightMargin: 10

        tooltip: "Close this dialog box"

        style: ButtonStyle{
            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 25
                radius: 3
                color: "#D22"
            }
        }

        onClicked:
        {
            base.close();
        }
    }

    //Text "Size: "
    Text
    {
        id: text_size
        text: catalog.i18nc("@label", "Size:")
        font.family: "Arial"
        font.pointSize: 12
        color: "#131151"

        anchors.top: close_button.top
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.leftMargin: 10
    }

    //User input of height
    TextField
    {
        id: size_input
        width: 80
        text: sizeInput
		// "ie. 20.0"

        anchors.top: text_size.top
        anchors.topMargin: -2
        anchors.left: text_size.right
        anchors.leftMargin: 10

		font.family: "Arial"
        font.pointSize: 12

        // Validate entered value
        Keys.onReturnPressed:
        {
			event.accepted = true
        }

        // Return the new entered value
        Keys.onReleased:
        {
            manager.sizeEntered(size_input.text)
        }
    }

    // Text: "mm"
    Text
    {
        id: text_unit
        text: "mm"
        font.family: "Arial"
        font.pointSize: 12
        color: "#131151"

        anchors.bottom: text_size.bottom
        anchors.bottomMargin: 0
        anchors.left: size_input.right
        anchors.leftMargin: 5
    }


    //Textfield for User Messages
    Text
    {
        id: user_text

        width: 280
        anchors.top: parent.top
        anchors.topMargin: 2
        anchors.left: parent.left
        anchors.leftMargin: 10

        text: userInfoText

        font.family: "Arial"
        font.pointSize: 10
        //The color gets overwritten by the html tags added to the text
        color: "black"

        wrapMode: Text.Wrap
    }

}
