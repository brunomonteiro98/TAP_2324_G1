'App teste
'15/03/2024

Imports System.IO.Ports
Imports System.Text
Imports System.Math
Imports Newtonsoft.Json

Public Class Form1
    Dim incremento As Decimal
    Dim selected As String
    Dim sendselected As Boolean = False

    Private Sub btnay_Click(sender As Object, e As EventArgs) Handles btnay.Click
        selected = "ay"
        Timer1.Enabled = True
    End Sub

    Private Sub btnaz_Click(sender As Object, e As EventArgs) Handles btnaz.Click
        selected = "az"
        Timer1.Enabled = True
    End Sub

    Private Sub btnrx_Click(sender As Object, e As EventArgs) Handles btnrx.Click
        selected = "rx"
        Timer1.Enabled = True
    End Sub

    Private Sub btnry_Click(sender As Object, e As EventArgs) Handles btnry.Click
        selected = "ry"
        Timer1.Enabled = True
    End Sub

    Private Sub btnExit_Click(sender As Object, e As EventArgs) Handles btnExit.Click
        Me.Close()
    End Sub

    Private Sub btnstop_Click(sender As Object, e As EventArgs) Handles btnstop.Click
        Timer1.Enabled = False
        sendselected = False
        txtbxax.Enabled = True
        txtbxay.Enabled = True
        txtbxaz.Enabled = True
        txtbxrx.Enabled = True
        txtbxry.Enabled = True
        txtbxrz.Enabled = True
        txtbxIncremento.Enabled = True
    End Sub

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        txtbxax.Enabled = False
        txtbxay.Enabled = False
        txtbxaz.Enabled = False
        txtbxrx.Enabled = False
        txtbxry.Enabled = False
        txtbxrz.Enabled = False
        txtbxIncremento.Enabled = False
        If sendselected Then
            Dim data = (CDec(txtbxax.Text) / 10, CDec(txtbxay.Text) / 10, CDec(txtbxaz.Text) / 10, CDec(txtbxrx.Text) / 10, CDec(txtbxry.Text) / 10, CDec(txtbxrz.Text) / 10)
            send(data)
        Else
            Dim data = sendIncrementos(selected)
            send(data)
        End If
    End Sub

    Private Sub btnrz_Click(sender As Object, e As EventArgs) Handles btnrz.Click
        selected = "rz"
        Timer1.Enabled = True
    End Sub

    Private Sub btnax_Click(sender As Object, e As EventArgs) Handles btnax.Click
        selected = "ax"
        Timer1.Enabled = True
    End Sub

    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles Me.Load
        With SerialPort1
            .PortName = "COM1"
            .BaudRate = 115200
            .Parity = Parity.None
            .DataBits = 8
            .StopBits = StopBits.One
            .Encoding = Encoding.UTF8
        End With
        txtbxax.Text = 0
        txtbxay.Text = 0
        txtbxaz.Text = 0
        txtbxrx.Text = 0
        txtbxry.Text = 0
        txtbxrz.Text = 0
        txtbxIncremento.Text = 2
        selected = ""
        Me.BackgroundImage = Image.FromFile("Image.png")
        Me.BackgroundImageLayout = ImageLayout.Center
        Me.Icon = New Icon("Icon.ico")
        Me.MaximizeBox = False
        Me.FormBorderStyle = FormBorderStyle.Fixed3D
        Timer1.Interval = 40
        Timer1.Enabled = False
    End Sub

    Private Sub btnSend_Click(sender As Object, e As EventArgs) Handles btnSend.Click
        If Abs(CDec(txtbxax.Text)) Or Abs(CDec(txtbxay.Text)) Or Abs(CDec(txtbxaz.Text)) Or Abs(CDec(txtbxrx.Text)) Or Abs(CDec(txtbxry.Text)) Or Abs(CDec(txtbxrz.Text)) > 10 Then
            If CDec(txtbxax.Text) < 0 Then
                txtbxax.Text = -10
            ElseIf CDec(txtbxax.Text) > 10 Then
                txtbxax.Text = 10
            ElseIf CDec(txtbxay.Text) < 0 Then
                txtbxay.Text = -10
            ElseIf CDec(txtbxay.Text) > 10 Then
                txtbxay.Text = 10
            ElseIf CDec(txtbxaz.Text) < 0 Then
                txtbxaz.Text = -10
            ElseIf CDec(txtbxaz.Text) > 10 Then
                txtbxaz.Text = 10
            ElseIf CDec(txtbxrx.Text) < 0 Then
                txtbxrx.Text = -10
            ElseIf CDec(txtbxrx.Text) > 10 Then
                txtbxrx.Text = 10
            ElseIf CDec(txtbxry.Text) < 0 Then
                txtbxry.Text = -10
            ElseIf CDec(txtbxry.Text) > 10 Then
                txtbxry.Text = 10
            ElseIf CDec(txtbxrz.Text) < 0 Then
                txtbxrz.Text = -10
            ElseIf CDec(txtbxrz.Text) > 10 Then
                txtbxrz.Text = 10
            End If
        End If
        sendselected = True
        Timer1.Enabled = True
    End Sub
    Private Sub send(data)
        If SerialPort1.IsOpen Then
            Dim json = JsonConvert.SerializeObject(data)
            SerialPort1.WriteLine(json)
            SerialPort1.Close()
        Else
            SerialPort1.Open()
            Dim json = JsonConvert.SerializeObject(data)
            SerialPort1.WriteLine(json)
            SerialPort1.Close()
        End If
    End Sub
    Function sendIncrementos(selected)
        incremento = CDec(txtbxIncremento.Text)
        If Abs(incremento) > 10 Then
            If incremento < 0 Then
                incremento = -10
            Else
                incremento = 10
            End If
            txtbxIncremento.Text = incremento
        End If
        incremento /= 10
        Select Case selected
            Case "ax"
                Dim data = (incremento, 0, 0, 0, 0, 0)
                Return data
            Case "ay"
                Dim data = (0, incremento, 0, 0, 0, 0)
                Return data
            Case "az"
                Dim data = (0, 0, incremento, 0, 0, 0)
                Return data
            Case "rx"
                Dim data = (0, 0, 0, incremento, 0, 0)
                Return data
            Case "ry"
                Dim data = (0, 0, 0, 0, incremento, 0)
                Return data
            Case "rz"
                Dim data = (0, 0, 0, 0, 0, incremento)
                Return data
        End Select
        Return False
    End Function
End Class
