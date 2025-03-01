
import segno

link = "https://docs.google.com/forms/d/e/1FAIpQLSfOOQhKHwEfpM0uXJ-hfeUSGFjNv8B21JVGAnsSWvNsgYfK4Q/viewform"
segno.make_qr(link).save("qr_code.png", scale=5)