import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 (브라우저 탭 이름 등)
st.set_page_config(page_title="성심당 빵 백과사전", layout="wide")

# 2. 우리가 만든 HTML/CSS/JS 코드 (파이썬 변수에 담기)
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>성심당 빵 백과사전</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; }
        .bread-card { transition: all 0.3s ease; }
        .bread-card:hover { transform: translateY(-10px); }
    </style>
</head>
<body class="bg-orange-50 p-4 md:p-8">

    <header class="text-center mb-12">
        <h1 class="text-4xl font-bold text-orange-800 mb-2">🥖 성심당 명예의 전당</h1>
        <p class="text-gray-600">티스토리 블로그와 연동된 실시간 빵 정보</p>
        <div class="h-1 w-24 bg-orange-400 mx-auto mt-4"></div>
    </header>

    <div id="bread-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        </div>

    <script>
        const breadData = [
            { id: 1, name: "마라미고로케", link: "https://travelbuddy-korea.tistory.com/2", desc: "매콤한 마라향이 가득한 특별한 고로케", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" },
            { id: 2, name: "뺑오쇼콜라", link: "https://travelbuddy-korea.tistory.com/3", desc: "겹겹이 쌓인 페이스트리 속 달콤한 초콜릿", img: "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=400" },
            { id: 3, name: "모찌모찌식빵", link: "https://travelbuddy-korea.tistory.com/4", desc: "이름처럼 쫄깃쫄깃한 식감이 일품인 식빵", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" },
            { id: 4, name: "야채고로케", link: "https://travelbuddy-korea.tistory.com/5", desc: "아삭한 야채와 고소한 튀김의 환상 궁합", img: "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=400" },
            { id: 5, name: "작은메아리", link: "https://travelbuddy-korea.tistory.com/6", desc: "보문산메아리의 미니 버전, 바삭하고 달콤함", img: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400" },
            { id: 6, name: "노아레즌", link: "https://travelbuddy-korea.tistory.com/7", desc: "건포도와 호두가 듬뿍 들어간 건강 호밀빵", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" },
            { id: 7, name: "시월의무화과", link: "https://travelbuddy-korea.tistory.com/8", desc: "톡톡 터지는 무화과의 풍미가 가득한 계절빵", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" },
            { id: 8, name: "빅매치", link: "https://travelbuddy-korea.tistory.com/9", desc: "겉은 비스킷, 속은 크림치즈로 가득한 인기 메뉴", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" },
            { id: 9, name: "무화과그늘아래", link: "https://travelbuddy-korea.tistory.com/10", desc: "호두와 무화과가 조화로운 고소한 건강빵", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" },
            { id: 10, name: "스테이크빵", link: "https://travelbuddy-korea.tistory.com/11", desc: "든든한 스테이크 속재료가 듬뿍 들어간 조리빵", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400" }
        ];

        const grid = document.getElementById('bread-grid');

        breadData.forEach(bread => {
            const card = `
                <div class="bread-card bg-white rounded-2xl shadow-md overflow-hidden border border-orange-100 flex flex-col">
                    <div class="h-48 bg-gray-200 relative">
                         <img src="${bread.img}" class="w-full h-full object-cover" alt="${bread.name}">
                         <div class="absolute top-2 left-2 bg-orange-500 text-white text-xs px-2 py-1 rounded">No.${bread.id}</div>
                    </div>
                    <div class="p-6 flex flex-col flex-grow">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">${bread.name}</h3>
                        <p class="text-gray-600 text-sm mb-6 flex-grow leading-relaxed">${bread.desc}</p>
                        <a href="${bread.link}" target="_blank" 
                           class="inline-block w-full text-center bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-4 rounded-xl transition-colors shadow-sm">
                           상세 레시피/후기 보기
                        </a>
                    </div>
                </div>
            `;
            grid.innerHTML += card;
        });
    </script>
</body>
</html>
"""

# 3. Streamlit을 통해 HTML 렌더링하기
components.html(html_code, height=2000, scrolling=True)
