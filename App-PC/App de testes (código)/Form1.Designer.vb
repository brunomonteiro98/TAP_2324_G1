<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Me.btnax = New System.Windows.Forms.Button()
        Me.txtbxax = New System.Windows.Forms.TextBox()
        Me.txtbxay = New System.Windows.Forms.TextBox()
        Me.txtbxrz = New System.Windows.Forms.TextBox()
        Me.txtbxaz = New System.Windows.Forms.TextBox()
        Me.txtbxrx = New System.Windows.Forms.TextBox()
        Me.txtbxry = New System.Windows.Forms.TextBox()
        Me.btnay = New System.Windows.Forms.Button()
        Me.btnaz = New System.Windows.Forms.Button()
        Me.btnrx = New System.Windows.Forms.Button()
        Me.btnry = New System.Windows.Forms.Button()
        Me.btnrz = New System.Windows.Forms.Button()
        Me.btnSend = New System.Windows.Forms.Button()
        Me.txtbxIncremento = New System.Windows.Forms.TextBox()
        Me.Label7 = New System.Windows.Forms.Label()
        Me.SerialPort1 = New System.IO.Ports.SerialPort(Me.components)
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        Me.btnExit = New System.Windows.Forms.Button()
        Me.btnstop = New System.Windows.Forms.Button()
        Me.SuspendLayout()
        '
        'btnax
        '
        Me.btnax.Location = New System.Drawing.Point(12, 60)
        Me.btnax.Name = "btnax"
        Me.btnax.Size = New System.Drawing.Size(75, 25)
        Me.btnax.TabIndex = 0
        Me.btnax.Text = "ax"
        Me.btnax.UseVisualStyleBackColor = True
        '
        'txtbxax
        '
        Me.txtbxax.Location = New System.Drawing.Point(12, 89)
        Me.txtbxax.Name = "txtbxax"
        Me.txtbxax.Size = New System.Drawing.Size(75, 22)
        Me.txtbxax.TabIndex = 1
        '
        'txtbxay
        '
        Me.txtbxay.Location = New System.Drawing.Point(93, 89)
        Me.txtbxay.Name = "txtbxay"
        Me.txtbxay.Size = New System.Drawing.Size(75, 22)
        Me.txtbxay.TabIndex = 3
        '
        'txtbxrz
        '
        Me.txtbxrz.Location = New System.Drawing.Point(417, 89)
        Me.txtbxrz.Name = "txtbxrz"
        Me.txtbxrz.Size = New System.Drawing.Size(75, 22)
        Me.txtbxrz.TabIndex = 4
        '
        'txtbxaz
        '
        Me.txtbxaz.Location = New System.Drawing.Point(174, 89)
        Me.txtbxaz.Name = "txtbxaz"
        Me.txtbxaz.Size = New System.Drawing.Size(75, 22)
        Me.txtbxaz.TabIndex = 5
        '
        'txtbxrx
        '
        Me.txtbxrx.Location = New System.Drawing.Point(255, 89)
        Me.txtbxrx.Name = "txtbxrx"
        Me.txtbxrx.Size = New System.Drawing.Size(75, 22)
        Me.txtbxrx.TabIndex = 6
        '
        'txtbxry
        '
        Me.txtbxry.Location = New System.Drawing.Point(336, 89)
        Me.txtbxry.Name = "txtbxry"
        Me.txtbxry.Size = New System.Drawing.Size(75, 22)
        Me.txtbxry.TabIndex = 7
        '
        'btnay
        '
        Me.btnay.Location = New System.Drawing.Point(93, 60)
        Me.btnay.Name = "btnay"
        Me.btnay.Size = New System.Drawing.Size(75, 25)
        Me.btnay.TabIndex = 14
        Me.btnay.Text = "ay"
        Me.btnay.UseVisualStyleBackColor = True
        '
        'btnaz
        '
        Me.btnaz.Location = New System.Drawing.Point(174, 60)
        Me.btnaz.Name = "btnaz"
        Me.btnaz.Size = New System.Drawing.Size(75, 25)
        Me.btnaz.TabIndex = 15
        Me.btnaz.Text = "az"
        Me.btnaz.UseVisualStyleBackColor = True
        '
        'btnrx
        '
        Me.btnrx.Location = New System.Drawing.Point(255, 60)
        Me.btnrx.Name = "btnrx"
        Me.btnrx.Size = New System.Drawing.Size(75, 25)
        Me.btnrx.TabIndex = 16
        Me.btnrx.Text = "rx"
        Me.btnrx.UseVisualStyleBackColor = True
        '
        'btnry
        '
        Me.btnry.Location = New System.Drawing.Point(336, 60)
        Me.btnry.Name = "btnry"
        Me.btnry.Size = New System.Drawing.Size(75, 25)
        Me.btnry.TabIndex = 17
        Me.btnry.Text = "ry"
        Me.btnry.UseVisualStyleBackColor = True
        '
        'btnrz
        '
        Me.btnrz.Location = New System.Drawing.Point(417, 60)
        Me.btnrz.Name = "btnrz"
        Me.btnrz.Size = New System.Drawing.Size(75, 25)
        Me.btnrz.TabIndex = 18
        Me.btnrz.Text = "rz"
        Me.btnrz.UseVisualStyleBackColor = True
        '
        'btnSend
        '
        Me.btnSend.Location = New System.Drawing.Point(498, 88)
        Me.btnSend.Name = "btnSend"
        Me.btnSend.Size = New System.Drawing.Size(75, 25)
        Me.btnSend.TabIndex = 19
        Me.btnSend.Text = "Send"
        Me.btnSend.UseVisualStyleBackColor = True
        '
        'txtbxIncremento
        '
        Me.txtbxIncremento.Location = New System.Drawing.Point(12, 30)
        Me.txtbxIncremento.Name = "txtbxIncremento"
        Me.txtbxIncremento.Size = New System.Drawing.Size(75, 22)
        Me.txtbxIncremento.TabIndex = 20
        '
        'Label7
        '
        Me.Label7.AutoSize = True
        Me.Label7.Location = New System.Drawing.Point(99, 33)
        Me.Label7.Name = "Label7"
        Me.Label7.Size = New System.Drawing.Size(231, 16)
        Me.Label7.TabIndex = 21
        Me.Label7.Text = "Incremento (aceita valores negativos)"
        '
        'Timer1
        '
        '
        'btnExit
        '
        Me.btnExit.Location = New System.Drawing.Point(498, 29)
        Me.btnExit.Name = "btnExit"
        Me.btnExit.Size = New System.Drawing.Size(75, 25)
        Me.btnExit.TabIndex = 22
        Me.btnExit.Text = "&Exit"
        Me.btnExit.UseVisualStyleBackColor = True
        '
        'btnstop
        '
        Me.btnstop.Location = New System.Drawing.Point(498, 60)
        Me.btnstop.Name = "btnstop"
        Me.btnstop.Size = New System.Drawing.Size(75, 25)
        Me.btnstop.TabIndex = 23
        Me.btnstop.Text = "Stop"
        Me.btnstop.UseVisualStyleBackColor = True
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(8.0!, 16.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(585, 138)
        Me.Controls.Add(Me.btnstop)
        Me.Controls.Add(Me.btnExit)
        Me.Controls.Add(Me.Label7)
        Me.Controls.Add(Me.txtbxIncremento)
        Me.Controls.Add(Me.btnSend)
        Me.Controls.Add(Me.btnrz)
        Me.Controls.Add(Me.btnry)
        Me.Controls.Add(Me.btnrx)
        Me.Controls.Add(Me.btnaz)
        Me.Controls.Add(Me.btnay)
        Me.Controls.Add(Me.txtbxry)
        Me.Controls.Add(Me.txtbxrx)
        Me.Controls.Add(Me.txtbxaz)
        Me.Controls.Add(Me.txtbxrz)
        Me.Controls.Add(Me.txtbxay)
        Me.Controls.Add(Me.txtbxax)
        Me.Controls.Add(Me.btnax)
        Me.Name = "Form1"
        Me.Text = "App teste"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents btnax As Button
    Friend WithEvents txtbxax As TextBox
    Friend WithEvents txtbxay As TextBox
    Friend WithEvents txtbxrz As TextBox
    Friend WithEvents txtbxaz As TextBox
    Friend WithEvents txtbxrx As TextBox
    Friend WithEvents txtbxry As TextBox
    Friend WithEvents btnay As Button
    Friend WithEvents btnaz As Button
    Friend WithEvents btnrx As Button
    Friend WithEvents btnry As Button
    Friend WithEvents btnrz As Button
    Friend WithEvents btnSend As Button
    Friend WithEvents txtbxIncremento As TextBox
    Friend WithEvents Label7 As Label
    Friend WithEvents SerialPort1 As IO.Ports.SerialPort
    Friend WithEvents Timer1 As Timer
    Friend WithEvents btnExit As Button
    Friend WithEvents btnstop As Button
End Class
