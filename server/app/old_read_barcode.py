
BUF_FILE_PATH = r'./bookshelf/buf.csv'


# def get_internal_id(img: Image):
#     k = cv2.waitKey(1)&0xff
#     if k == 27:
#         break
    
#     elif k == 13:
#         pixel_rgb_avg = np.mean(frame, axis=2)
#         frame[:,:,1] = np.where(frame[:,:,1] > pixel_rgb_avg*1.6, 255, frame[:,:,1])
        
#         frame_gray_scale = frame[:,:,0] = np.mean(frame, axis=2)
#         frame_gray_scale = frame[:,:,1] = np.mean(frame, axis=2)
#         frame_gray_scale = frame[:,:,2] = np.mean(frame, axis=2)
        
#         rgb_min = np.min(frame_gray_scale)
#         rgb_median = np.median(frame_gray_scale)
#         rgb_mean = np.mean(frame_gray_scale)
#         rgb_max = np.max(frame_gray_scale)
#         # cv2.imwrite("out/gray.jpg", frame_gray_scale)
        
#         threshold_while = rgb_median + 40
#         threshold_while = 170
#         frame_high_contrast = sigmoid(frame_gray_scale - (rgb_min + rgb_median//2.7)) * 255
#         # frame_high_contrast = np.where(frame_gray_scale > threshold_while, 255, frame_gray_scale)
#         # threshold_black = rgb_min + (rgb_max-rgb_min)//3
#         # threshold_black = 85
#         # print(threshold_black)
#         # frame_high_contrast = np.where(frame_high_contrast <= threshold_black, 0, frame_high_contrast)
#         d = decode(frame_high_contrast)
#         cv2.imwrite("out/high_contrast.jpg", frame_high_contrast)
        
#         img = Image.open("./out/high_contrast.jpg", "r")
#         ret = tesser.image_to_string(img)
        
#         code = extract_numbers(ret, 8)

def cam_capture(method:str = "internal_id"):
    
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    bookshelf = Bookshelf()
    
    try: 
        with open(BUF_FILE_PATH, mode='r', encoding='utf-8', newline='') as buf:
            reader = csv.reader(buf, delimiter=',')
            i = 0
            for row in reader:
                if i > 0:
                    bookshelf.add_book(row[0], row[1], row[2], row[3], row[4], row[5])
                i += 1
            print("loading bookshelf completed!")
    except:
        with open(BUF_FILE_PATH, mode='w', encoding='utf-8', newline='') as buf:
            writer = csv.writer(buf, delimiter=',')
            
            writer.writerow(["isbn", "internal_id", "title", "author", "publisher", "category"])
        print("new bookshelf csv created!")
    
    print(bookshelf)

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            d = decode(frame)
            
            # print(d)
            
            # if method == "internal_id":
                

            if d:
                for barcode in d:
                    barcode_data = barcode.data.decode('utf-8')
                    
                    # print(barcode_data)

                    if is_isbn(barcode_data):
                        
                        if not bookshelf.is_in_bookshelf(barcode_data):

                            winsound.Beep(2000, 50)
                            font_color = (0, 0, 255)
                            result = fetch_book_data(barcode_data)
                            
                            print(result)
                            bookshelf.add_book(result[0], "", result[1], result[2], result[3], result[4])

                            with open(BUF_FILE_PATH, 
                                      mode='a', 
                                      encoding='utf-8', 
                                      newline='') as buf:
                                writer = csv.writer(buf, delimiter=',')
                                writer.writerow(list(result))
                        else:
                            font_color = (0, 154, 87)

                        x, y, w, h = barcode.rect
                        cv2.rectangle(frame, (x, y), (x + w, y + h), font_color, 2)
                        frame = cv2.putText(frame, barcode_data, (x, y - 10), 
                                            font, .5, font_color, 2, cv2.LINE_AA)

        cv2.imshow('BARCODE READER Press Q -> Exit', frame)

        k = cv2.waitKey(1)&0xff
        if k == 27:
            break
        
        elif k == 13:
            pixel_rgb_avg = np.mean(frame, axis=2)
            frame[:,:,1] = np.where(frame[:,:,1] > pixel_rgb_avg*1.6, 255, frame[:,:,1])
            
            frame_gray_scale = frame[:,:,0] = np.mean(frame, axis=2)
            frame_gray_scale = frame[:,:,1] = np.mean(frame, axis=2)
            frame_gray_scale = frame[:,:,2] = np.mean(frame, axis=2)
            
            rgb_min = np.min(frame_gray_scale)
            rgb_median = np.median(frame_gray_scale)
            rgb_mean = np.mean(frame_gray_scale)
            rgb_max = np.max(frame_gray_scale)
            # cv2.imwrite("out/gray.jpg", frame_gray_scale)
            
            threshold_while = rgb_median + 40
            threshold_while = 170
            frame_high_contrast = sigmoid(frame_gray_scale - (rgb_min + rgb_median//2.7)) * 255
            # frame_high_contrast = np.where(frame_gray_scale > threshold_while, 255, frame_gray_scale)
            # threshold_black = rgb_min + (rgb_max-rgb_min)//3
            # threshold_black = 85
            # print(threshold_black)
            # frame_high_contrast = np.where(frame_high_contrast <= threshold_black, 0, frame_high_contrast)
            d = decode(frame_high_contrast)
            cv2.imwrite("out/high_contrast.jpg", frame_high_contrast)
            
            img = Image.open("./out/high_contrast.jpg", "r")
            ret = tesser.image_to_string(img)
            
            code = extract_numbers(ret, 8)
            print(code)
            
            if d:
                for barcode in d:
                    barcode_data = barcode.data.decode('utf-8')
                    print(barcode_data)

                    if is_resourse(barcode_data):
                        cv2.imwrite("out/high_contrast.jpg", frame_high_contrast)
                        
                        print("median:",rgb_median)
                        print("mean:", rgb_mean)
                        print("max:", rgb_max)
                        print("min:", rgb_min)
                        # print("threshold_black:", threshold_black)
                        print(barcode_data)
                        winsound.Beep(2000, 50)


    cap.release()

def extract_numbers(input_string, num_digits):
    pattern = r'\d{' + str(num_digits) + '}'
    match = re.findall(pattern, input_string)
    return match

def fetch_book_data(isbn):
    endpoint = 'https://iss.ndl.go.jp/api/sru'
    params = {'operation': 'searchRetrieve',
              'query': f'isbn="{isbn}"',
              'recordPacking': 'xml'}

    res = requests.get(endpoint, params=params)

    root = et.fromstring(res.text)
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
    title = root.find('.//dc:title', ns).text
    creator = root.find('.//dc:creator', ns).text
    publisher = root.find('.//dc:publisher', ns).text
    subject = root.find('.//dc:subject', ns).text

    return isbn, title, creator, publisher, subject

def sigmoid(x):
    return 1/(1+np.exp(-1*x))

def is_resourse(code):
    return len(code) == 8

def is_isbn(code):
    return len(code) == 13 and code[:3] == '978'

def getCamIndex():
    import os
    devs = os.listdir('/dev')
    vid_indices = [int(dev[-1]) for dev in devs 
                if dev.startswith('video')]
    vid_indices = sorted(vid_indices)
    print(vid_indices)

if __name__ == '__main__':
    cam_capture()
    # getCamIndex()