// MainPage.tsx
import React from 'react';
import Sidebar from '../blocks/Sidebar';
import styled from 'styled-components';
import '../../assets/fonts/Font.css';
import Card from '../blocks/Card';
import homeMan from '../../assets/images/homeman.svg'; // 아이콘 이미지를 로컬 파일로 추가
import { useNavigate } from 'react-router-dom'; // useNavigate 훅을 임포트

const MainPage: React.FC = () => {
    const cardData = [
        {
          title: '간단 교육자료',
          subtitle: '작업전 10분, 공장·설비별로 필수사항만 담은 안전교육 자료를 제공합니다.',
          content: ['공정, 기계별 교육자료', '사업장 위험요인 추출', '재해 대응 프로세스', '다국어 지원'],
          buttonText: '제작하기',
          buttonLink: '/tenMin'
        },
        {
          title: '정기 교육자료',
          subtitle: '산업안전보건법의 정기교육 기준을 준수하는 기업 맞춤형 자료를 제공합니다.',
          content: ['산업안전보건법 기준', '사업장의 근로자 대상', '사업장 특성 · 요구 반영', '다국어 지원'],
          buttonText: '제작하기',
          buttonLink: '../pages/FirstPage'
        },
        {
          title: '신규 교육자료',
          subtitle: '산업안전보건법의 신규작업 교육 기준을 준수하는 기업 맞춤형 자료를 제공합니다.',
          content: ['신규', '사업장 특성 · 요구 반영', '다국어 지원'],
          buttonText: '제작하기',
          buttonLink: '../pages/FirstPage'
        },
        {
          title: '특별 교육자료',
          subtitle: '산업안전보건법의 특별교육 기준을 준수하는 기업 맞춤형 자료를 제공합니다.',
          content: ['산업안전보건법 기준', '유해/위험 작업 근로자', '사업장 특성 · 요구 반영', '다국어 지원'],
          buttonText: '제작하기',
          buttonLink: '../pages/FirstPage'
        }
    ];
  return (
    <Container>
      <Sidebar />
      <Spacer />
      <Content>
        <Title>
          <span style={{ color: "#027b8b" }}>모두</span>
          <span>를 위한</span><br />
          <span style={{ color: "#027b8b" }}>현장 </span>
          <span>맞춤 </span><br />
          <span style={{ color: "#027b8b" }}>안전교육자료</span>
        </Title>
        <SubTitle>
            <SubtitleSpan>기업 맞춤형 안전 교육자료</SubtitleSpan><br />
            <SubtitleSpan>AI기반 작업장 위험요인 추출</SubtitleSpan><br />
            <SubtitleSpan>다국어 지원</SubtitleSpan><br />
        </SubTitle>
        <CardContainer>
          {cardData.map((card, index) => (
            <Card key={index} {...card} />
          ))}
        </CardContainer>
      </Content>
      <ImageBox>
          <img src={homeMan} alt="homeman" />
      </ImageBox>

      
    </Container>
  );
};

export default MainPage;

const Container = styled.div`
  display: flex;
`;

const Spacer = styled.div`
  width: 140px;
`;

const Content = styled.div`
  width: 348px;
  height: 550px;
  margin-top: 40px;
  background-color: #fff;
  justify-content: space-between;
  flex-direction: column;
  align-items: flex-start; /* 왼쪽 정렬 */
`;

const Title = styled.h1`
  margin-top: 60px; /* 추가적인 여백 제거 */
  margin-bottom: 20px; /* 하단 여백 설정 */
  font-family: 'Pretendard-SemiBold';
  font-size: 45px; /* 필요에 따라 조정 */
  color: #000000; /* 테마 색상 적용 */
  text-align: left;
`;

const SubTitle = styled.div`
  margin-top: 0px; /* 추가적인 여백 제거 */
  margin-bottom: 0px; /* 하단 여백 설정 */
  font-family: 'Pretendard-Light';
  font-size: 1.5em; /* 필요에 따라 조정 */
  color: #000000; /* 테마 색상 적용 */
  text-align: left;

   & > p {
    margin-bottom: 5px; /* 각 요소 사이의 간격 설정 */
  }
`;

const SubtitleSpan = styled.span`
  margin-bottom: 6px; /* 요소 사이의 세로 간격 조정 */
  display: inline-block; /* 줄 바꿈 시 간격 유지 */
  font-size: inherit;
  font-weight: inherit;
`;

const ImageBox = styled.div`
  margin-top: 22px;
  padding: 1rem 1rem 11rem 0rem;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;

  img {
    max-width: 90%;
    max-height: 100%;
    object-fit: contain;  /* 이미지 비율을 유지하면서 컨테이너 안에 맞춤 */
  }
`;

const CardContainer = styled.div`
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 40px;
`;

