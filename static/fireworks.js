
// 1. 불꽃놀이 함수 정의
function showFireworks() {
    const fireworksContainer = document.getElementById('fireworks');
    const message = document.getElementById('message');
    message.style.display = 'block';
    const images = [
        '/static/images/firework1.png',
        '/static/images/firework2.png',
        '/static/images/firework3.png',
        // 추가 이미지 파일 경로
    ];
    // 2. 스무개의 이미지가 램덤위치에서 나오게 설정
    for (let i = 0; i < 20; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';
        firework.style.top = Math.random() * 100 + 'vh';
        firework.style.left = Math.random() * 100 + 'vw';
        firework.style.backgroundImage = `url(${images[Math.floor(Math.random() * images.length)]})`;
        fireworksContainer.appendChild(firework);
        setTimeout(() => firework.remove(), 3000);
    }
    setTimeout(() => {
        message.style.display = 'none';
    }, 4000);
}

 // 3. 모든 체크박스가 체크되었을 때, showFireworks() 작동

document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
            if (allChecked) {
                showFireworks();
            }
        });
    });
});