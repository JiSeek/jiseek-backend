from darknet_images import main


def get_result(filename):
    
    result = main(filename)
    print(result)

    return result

if __name__ == "__main__":
    
    # 사용자가 검색을 요청한 이미지의 주소가 필요합니다. S3버킷의 폴더/파일명 형태"
    filename = "img/rice.jpg"
    
    get_result(filename)
