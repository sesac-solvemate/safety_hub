// Card.tsx
import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import checkcircle from '../../assets/images/checkcircle.svg';

interface CardProps {
    title: string;
    subtitle: string;
    content: string[];
    buttonText: string;
    buttonLink: string;
}

const Card: React.FC<CardProps> = ({ title, subtitle, content, buttonText, buttonLink }) => {
    const navigate = useNavigate();
    
    const handleButtonClick = () => {
        navigate(buttonLink);
    };

    return (
      <StyledCard>
        <CardTitle>{title}</CardTitle>
        <CardSubtitle>{subtitle}</CardSubtitle>
        <CardContent>
          {content.map((item, index) => (
            <CardContentItem key={index}>
              <Icon src={checkcircle} alt="checkcircle" /> {item}
            </CardContentItem>
          ))}
        </CardContent>
        <CardButton onClick={handleButtonClick}>{buttonText}</CardButton>
      </StyledCard>
    );
};

export default Card;

const StyledCard = styled.div`
    width: 217px;
    height: 360px;
    padding: 32px;
    margin: 5px;
    background-color: #fff;
    border: 1px solid #d9d9d9;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.3s ease, border-color 0.3s ease;

    &:hover {
        transform: scale(1.05);
        border-color: #027b8b;
    }
`;

const CardTitle = styled.h2`
    font-family: 'Pretendard-Bold';
    font-size: 24px;
    text-align: center;
    color: #1e1e1e;
    margin-bottom: 10px;
`;

const CardSubtitle = styled.p`
    font-size: 14px;
    text-align: left;
    color: #1e1e1e;
    margin-bottom: 20px;
`;

const CardContent = styled.ul`
    list-style: none;
    padding: 0;
    margin: 0 0 25px;
    width: 100%;
`;

const CardContentItem = styled.li`
    font-size: 12px;
    color: #757575;
    margin-bottom: 8px;
    display: flex;
    align-items: center;

    &::before {
        content: url('/path/to/icon.png'); // 아이콘 이미지 경로
        margin-right: 8px;
    }
`;

const CardButton = styled.button`
    background-color: #2c2c2c;
    color: #f5f5f5;
    font-size: 16px;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;

    &:hover {
        background-color: #027b8b;
    }
`;

const Icon = styled.img`
    width: 20px;
    height: 20px;
    margin-right: 8px;
`;
