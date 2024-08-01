// FirstPage.tsx
import React from 'react';
import Sidebar from '../blocks/Sidebar';
import styled from 'styled-components';
import '../../assets/fonts/Font.css';
import progressbar from '../../assets/images/progressbar.svg'; 
import CompanyForm from '../blocks/CompanyForm';

const FirstPage: React.FC = () => {
    return (
        <Container>
            <Sidebar />
            <FixedContainer>
                <ProgressBar>
                    <StyledImage src={progressbar} alt="Example" />
                </ProgressBar>
                <TextContainer>
                    <Title>
                        <span style={{ color: "#399AF9" }}>회사정보</span>
                        <span>를 입력해주세요</span><br />
                    </Title>
                    <Description>교육자료 생성을 위해 회사정보를 입력해주세요</Description>
                </TextContainer>
                <FormContainer>
                    <CompanyForm />
                </FormContainer>
            </FixedContainer>
        </Container>
    );
};

export default FirstPage;

const Container = styled.div`
  display: flex;
`;

const FixedContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: top;
  align-items: center;
  width: 918px;
  height: 100vh; /* 전체 화면 높이 */
  margin-top: 40px;
  margin-left: 116px; 
  padding: 20px;
  box-sizing: border-box;
`;

const ProgressBar = styled.div`
  width: 100%;
  margin-bottom: 20px;
`;

const StyledImage = styled.img`
  width: 100%;
  height: auto;
`;

const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 수직 정렬을 위로 설정 */
  align-items: flex-start; /* 수평 정렬을 왼쪽으로 설정 */
  width: 100%;
`;

const Title = styled.h1`
  font-family: 'Pretendard-Bold';
  font-size: 32px;
  margin-bottom: 10px;
`;

const Description = styled.p`
  font-size: 16px;
  font-family: 'Pretendard-Light';
  color: #757575;
  margin-top: 0px;
  margin-bottom: 30px;
  text-align: left; /* 왼쪽 정렬 */
  width: 80%;
`;

const FormContainer = styled.div`
  width: 100%;
  flex-grow: 1; /* 남은 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #F7F7FC;
  border-radius: 20px;
  margin-bottom: 80px; 
`;

