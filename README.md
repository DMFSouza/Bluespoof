# Bluespoof HUN73R.0047

<strong>Board designed by</strong> David Miguel (HUN73R.0047) (https://github.com/DMFSouza).
<br><br>
<strong>If you enjoyed this project, consider buying me a coffee:</strong>
<br>
<div align="center">
  <a href="https://www.buymeacoffee.com/davidmiguel">
    <img src="https://github.com/DMFSouza/EvilCrowRF_HUN73R.0047/blob/main/images/bmc_qr.png" alt="coffee" width="350" height="350">
  </a>
</div>
<br>
</ul>
<strong>To check the original Code:</strong> Salmg ( https://github.com/salmg/ViolentMag).


# Introduction<a id="introduction"></a>
The initial idea was to use a simple Bluetooth headset connected to an antenna to simulate magnetic stripe frequencies. For this, a basic headset was used. 
<br><br>
<div align="center">
  <img src="https://github.com/DMFSouza/Magspoof/blob/main/data/898e2897-2945-49ac-b6f6-38a5da553caa.jpg" width="50%">
</div>
<br><br>
During prototyping, a copper-clad phenolic board was used where, with the help of a pen, I drew the antenna design and marked where the headset and power source would be positioned.
<br>
<div align="center">
  <img src="https://github.com/DMFSouza/Magspoof/blob/main/data/ab573aa7-ce8b-439f-9b23-a83315ce5656.jpg" width="50%">
</div>
<br>
After completing the design, the board was etched with ferric chloride, resulting in something similar to this.
<br>
<div align="center">
  <img src="https://github.com/DMFSouza/Magspoof/blob/main/data/1f75f965-3eed-4fe9-ace5-d12154c74889.jpg" width="50%">
</div>
<br>
In the initial project, I intended to use a button cell module, but soon realized that this module would not provide the necessary current for the project.
<br>
<div align="center">
  <img src="https://github.com/DMFSouza/Magspoof/blob/main/data/295d5e79-9227-432a-b4ba-27324cd61ce1.jpg" width="50%">
</div>
<br>
So, I had to adapt a lithium battery connected to a USB Type-C input for charging. I also soldered a selector switch to control when the board is powered on or off. Everything was glued with hot glue; the appearance isn’t great, but it is functional.
<br>
<div align="center">
  <img src="https://github.com/DMFSouza/Magspoof/blob/main/data/WhatsApp%20Image%202024-08-17%20at%2019.04.53.jpeg" width="50%">
</div>
<br>
To convert the magnetic stripe code into audio that could emulate the same frequency, a Python script was used to convert the stripe information into a .WAV audio file. This file is played in a loop, turning the audio into magnetic information.
<br>
The final result can be seen in the video below where I used my test smartphone running Kali Nethunter on Corvus OS. The communication is instantaneous.
<br><br>
<div align="center">



https://github.com/user-attachments/assets/7f756582-3c41-4557-8386-d3658fc87949


</div>
<br>
<br>
This project is intended for educational and cybersecurity research purposes only. The author is not responsible for any misuse.
