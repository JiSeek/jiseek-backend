# 지 식(知食, JISEEK)
- AI 이미지 감지 및 분류 기능을 활용해 사용자가 업로드한 사진 속 메뉴를 분석하여 한식 400종류의 영양 성분과 레시피를 제공하는 서비스

## 1. 프로젝트 소개


- 타겟층
    - 한국 방문 중이거나 예정인 외국인 & 한식의 영양 정보 및 레시피에 관심이 있는 한국인

<br />

- 문제 정의
    - 코로나 이전부터 이미 K-POP, 영화 등의 컨텐츠를 중심으로 전세계적으로 한국에 대한 전반적인 관심이 급증하고 있었음
    - 코로나 종식 이후 한국 방문을 희망하는 여행객의 잠재 수요가 감지됨
    - 여행지에서 음식을 주문하는 경우 세부 정보를 알기 어려움
    - 자신이 주문한 음식 사진을 찍어서 SNS에 올리는 일은 일상화된 삶의 양식
    - 따라서 음식 사진을 찍어서 업로드하면 영양 성분과 관련 레시피(유튜브 영상)를 안내하는 서비스를 기획

<br />

- 목표
  - 사진 한 장으로 한식 관련 정보를 파악할 수 있도록 하여 외국인의 한식에 대한 접근성 향상

<br />

## 2. 프로젝트 환경


  - 기술 스택
    - python
    - PostgreSQL
  - [사용된 라이브러리](./Pipfile)
    - django
      - 인증, 관리와 같이 거의 대부분의 사이트에서 사용하는 기능들이 기본 모듈로 제공
      - drf를 사용하고자 함
    - djangorestframework
      - serialize가 용이
      - validation이나 security가 기본적으로 구현 되어있음
      - rest api를 개발 하는데 있어서, rest api 규약을 지킬수 있도록 편의기능을 제공

<br />

## 3. 프로젝트 기능 설명

  - 프론트엔드와 통신 가능한 REST API 개발
  - 프로젝트만의 차별점, 기대 효과

<br />

## 4. 프로젝트 구성도
  - 전체
  ![img1](https://reviewkingwordcloud.s3.ap-northeast-2.amazonaws.com/media/docs/jiseek_BE_Workflow.003.jpeg)
  - ERD
  ![img2](https://reviewkingwordcloud.s3.ap-northeast-2.amazonaws.com/media/docs/jiseek_BE_Workflow.004.png)
  - Infra
  ![img3](https://reviewkingwordcloud.s3.ap-northeast-2.amazonaws.com/media/docs/jiseek_BE_Workflow.001.jpeg)
  - Login
  ![img4](https://reviewkingwordcloud.s3.ap-northeast-2.amazonaws.com/media/docs/jiseek_BE_Workflow.002.jpeg)

<br />

## 5. 프로젝트 팀원 역할 분담
  | 이름 | 역할 | 담당 업무 |
  | ------ | ------ | ------ |
  | 고정현 | 팀장/백엔드 개발 | - DB schema 설계<br />\- 음식 정보 API 구현 <br />\- 게시판 및 댓글 CRUD API 구현 <br />\- Docker 환경 구현 <br />\- 서비스 배포 |
  | 김지훈 | 백엔드 개발 | - DB schema 설계<br />- 로그인/로그아웃/이메일 인증 API 구현<br />- 소셜 로그인/로그아웃(구글/네이버/카카오) API 구현<br />- 게시판 및 음식 좋아요/즐겨찾기 목록 API 구현<br />- 서비스 배포 |

<br />

## 6. 버전
  - v1(현재)

<br />

## 7. FAQ
  - 자주 받는 질문 정리