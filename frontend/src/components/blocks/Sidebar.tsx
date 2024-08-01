import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import theme from '../../assets/theme';
import settings from '../../assets/images/settings.svg'; 
import help from '../../assets/images/help.svg'; 
import history from '../../assets/images/history.svg'; 
import logo from '../../assets/images/logo.svg'; 

const Sidebar: React.FC = () => {
    const [items, setItems] = useState<string[]>([]);

//    useEffect(() => {
//         axios.get('https://api.example.com/items')
//             .then(response => {
//                 setItems(response.data);
//             })
//             .catch(error => {
//                 console.error('Error fetching data:', error);
//             });
//     }, []);

    return (
        <Container>
            <LogoBox>
                <img src={logo} alt="SafetyHub Logo" />
            </LogoBox>
            <NewItemButton>+ 새로 만들기</NewItemButton>
            <h4 style={{ display: 'flex', alignItems: 'center', color: '#B3B3B3', margin: '20px 10px 0px 0px'}}>
                <Icon src={history} alt="icon" />
                자료 목록
            </h4>
            <Line />
            <List>
                {items.map((item, index) => (
                    <ListItem key={index} onClick={() => console.log(item)}>
                        {item}
                    </ListItem>
                ))}
            </List>
            <BottomIcons>
                <IconWrapper>
                    <Icon src={settings} alt="settings" />
                    설정
                </IconWrapper>
                <IconWrapper>
                    <Icon src={help} alt="help" />
                    사용법
                </IconWrapper>
            </BottomIcons>
        </Container>
    );
};

export default Sidebar;

const Container = styled.div`
    width: 240px;
    height: 100vh;
    background-color: #F7F7FC;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 10px 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
`;

const LogoBox = styled.div`
    display: flex;
    justify-content: center;
    padding: 1rem 1rem 1rem 0rem;
    img {
        width: 210px; /* 로고 이미지 크기 조절 */
    }
`;

const NewItemButton = styled.button`
    background-color: #015477;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 1rem;
    margin: 0rem;
    width: 240px;
    cursor: pointer;
    text-align: left;
    font-size: 1rem;
    &:hover {
        background-color: #014663;
        box-shadow: 3px 0 3px rgba(0,0,0,0.1);
    }
`;

const Line = styled.hr`
  border: 0px;
  height: 1px;
  width: 230px;
  background: #B3B3B3;
`;

const List = styled.ul`
    list-style: none;
    padding: 0;
    flex-grow: 1;
`;

const ListItem = styled.li`
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    cursor: pointer;
    &:hover {
        color: #1E1E1E;
    }
`;

const Icon = styled.img`
    width: 24px;
    height: 24px;
    margin-right: 0.5rem;
`;

const BottomIcons = styled.div`
    display: flex;
    flex-direction: column;
    align-items: left;
    padding: 1rem 0;
`;

const IconWrapper = styled.div`
    display: flex;
    align-items: center;
    margin-top: 1rem;
    cursor: pointer;
    font-size: 1rem;
    color: #707070;
    &:hover {
        color: black;
    }
    ${Icon} {
        margin-right: 0.5rem;
    }
`;
