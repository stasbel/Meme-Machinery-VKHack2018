from PIL import ImageDraw
from PIL import ImageFont


class Printer:
    @staticmethod
    def print(image, text):
        image = image.copy()
        draw = ImageDraw.Draw(image)
        ww, hh = image.size
        font = ImageFont.truetype('impact.ttf', int(hh / 8))

        def draw_text(subtext, text_x, text_y):
            draw.text((text_x - 2, text_y - 2), subtext, (0, 0, 0), font=font)
            draw.text((text_x + 2, text_y - 2), subtext, (0, 0, 0), font=font)
            draw.text((text_x + 2, text_y + 2), subtext, (0, 0, 0), font=font)
            draw.text((text_x - 2, text_y + 2), subtext, (0, 0, 0), font=font)
            draw.text((text_x, text_y), subtext, (255, 255, 255), font=font)

        w, h = draw.textsize(text, font)

        if w > image.width:
            lineCount = int(round((w / image.width) + 1))

            lines = []
            if lineCount > 1:

                lastCut = 0
                isLast = False
                for i in range(0, lineCount):
                    if lastCut == 0:
                        cut = int(len(text) / lineCount) * i
                    else:
                        cut = lastCut

                    if i < lineCount - 1:
                        next_cut = int(len(text) / lineCount) * (i + 1)
                    else:
                        next_cut = len(text)
                        isLast = True

                    next_cut = int(next_cut)
                    if next_cut >= len(text) or text[next_cut] == " ":
                        pass
                    else:
                        while next_cut < len(text) and text[next_cut] != " ":
                            next_cut += 1

                    line = text[cut:next_cut].strip()

                    w, h = draw.textsize(line, font)
                    if not isLast and w > image.width:
                        next_cut -= 1
                        while next_cut < len(text) and text[next_cut] != " ":
                            next_cut -= 1

                    lastCut = next_cut
                    lines.append(text[cut:next_cut].strip())

            else:
                lines.append(text)

            for i in range(0, lineCount):
                w, h = draw.textsize(lines[i], font)
                draw_text(lines[i], image.width / 2 - w / 2, i * h)
        else:
            draw_text(text, image.width / 2 - w / 2, 10)

        return image
