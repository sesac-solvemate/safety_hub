import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import processJson from '../../assets/process.json'; // Ensure this path is correct

interface Process {
    id: number;
    name: string;
}

interface CompanyProcess {
    id: string;
    name: string;
}

const MaterialTypeForm: React.FC = () => {
    const [selection, setSelection] = useState<string | null>(null);
    const [keywords, setKeywords] = useState<(Process | CompanyProcess)[]>([]);
    const [loading, setLoading] = useState(false);
    const [showMore, setShowMore] = useState(false);
    const [selectedKeyword, setSelectedKeyword] = useState<Process | CompanyProcess | null>(null);
    const { guideId } = useParams<{ guideId: string }>();
    const navigate = useNavigate();

    useEffect(() => {
        if (selection) {
            setLoading(true);
            setTimeout(() => {
                const selectedKeywords = selection === 'work-process' ? processJson.process : processJson.companyProcess;
                setKeywords(selectedKeywords);
                setLoading(false);
            }, 2000); // Ensure at least 2 seconds of loading
        }
    }, [selection]);

    const handleSelection = (type: string) => {
        setSelection(type);
        setSelectedKeyword(null);
    };

    const handleKeywordClick = (keyword: Process | CompanyProcess) => {
        setSelectedKeyword(keyword);
    };

    const handleNextClick = () => {
        if (selectedKeyword) {
            axios.post(`/step/${guideId}/2`, { process: selectedKeyword.name, processId: selectedKeyword.id })
                .then(response => {
                    navigate('/SecondForm'); // Navigate to SecondForm on success
                })
                .catch(error => {
                    console.error(error);
                    navigate('/SecondForm'); // Navigate to SecondForm on failure
                });
        } else {
            navigate('/SecondForm'); // Navigate to SecondForm if no keyword is selected
        }
    };

    return (
        <FormContainer>
            <Label>
                어떤 기준으로 안전교육자료를 제작할 것인지 선택해주세요. <br />
            </Label>
            <ButtonContainer>
                <OptionButton
                    onClick={() => handleSelection('work-process')}
                    selected={selection === 'work-process'}
                >
                    작업 공정별
                </OptionButton>
                <OptionButton
                    onClick={() => handleSelection('machinery-equipment')}
                    selected={selection === 'machinery-equipment'}
                >
                    기계 설비별
                </OptionButton>
            </ButtonContainer>
            {selection && (
                <>
                    <Label>
                        안전교육이 필요한 {selection === 'work-process' ? '작업 공정을' : '기계 설비를'} 선택해주세요.
                    </Label>
                    {loading ? (
                        <LoadingMessage>! 데이터에서 작업 공정을 추출 중입니다. 잠시만 기다려주세요.</LoadingMessage>
                    ) : (
                        <>
                            <KeywordContainer>
                                {keywords.slice(0, showMore ? keywords.length : 5).map((keyword, index) => (
                                    <KeywordButton
                                        key={index}
                                        onClick={() => handleKeywordClick(keyword)}
                                        selected={selectedKeyword?.name === keyword.name}
                                    >
                                        {keyword.name}
                                    </KeywordButton>
                                ))}
                            </KeywordContainer>
                            {keywords.length > 5 && (
                                <ShowMoreButton onClick={() => setShowMore(!showMore)}>
                                    {showMore ? '간략히 보기' : '모두보기'}
                                </ShowMoreButton>
                            )}
                        </>
                    )}
                </>
            )}
            <ButtonContainerBottom>
                <NavButton onClick={() => navigate(-1)}>이전으로</NavButton>
                <NavButton disabled={!selectedKeyword} onClick={handleNextClick}>다음으로</NavButton>
            </ButtonContainerBottom>
        </FormContainer>
    );
};

export default MaterialTypeForm;

const FormContainer = styled.div`
    width: 85%;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: flex-start;
    padding: 30px 0px;
    align-items: flex-start;
    & > * {
        width: 100%; /* Ensure each child takes full width */
        margin-bottom: 10px; /* Add some spacing between elements */
    }
    position: relative;
`;

const ButtonContainer = styled.div`
    display: flex;
    justify-content: flex-start; /* Align buttons to the left */
    margin-bottom: 20px;
    & > * {
        margin-right: 10px; /* Add some spacing between buttons */
    }
`;

const ButtonContainerBottom = styled.div`
    display: flex;
    justify-content: flex-end; /* Align buttons to the right */
    margin-top: auto; /* Push the buttons to the bottom */
    & > * {
        margin-left: 10px; /* Add some spacing between buttons */
    }
`;

const OptionButton = styled.button<{ selected: boolean }>`
    background-color: ${({ selected }) => (selected ? '#027b8b' : '#f5f5f5')};
    color: ${({ selected }) => (selected ? '#fff' : '#000')};
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px 20px;
    margin-top: 20px;
    font-size: 16px;
    cursor: pointer;
    &:hover {
        background-color: ${({ selected }) => (selected ? '#025e6b' : '#ddd')};
    }
`;

const Label = styled.label`
    font-size: 16px;
    font-weight: bold;
    color: #333;
    text-align: left;
    margin-bottom: 0px;
`;

const LoadingMessage = styled.p`
    font-size: 14px;
    color: #757575;
    text-align: left;
    padding: 0px 5px;
`;

const KeywordContainer = styled.div`
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    margin-bottom: 20px;
`;

const KeywordButton = styled.button<{ selected: boolean }>`
    background-color: ${({ selected }) => (selected ? '#027b8b' : '#f5f5f5')};
    color: ${({ selected }) => (selected ? '#fff' : '#000')};
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px 20px;
    cursor: pointer;
    margin: 5px;
    &:hover {
        background-color: ${({ selected }) => (selected ? '#025e6b' : '#ddd')};
    }
`;

const ShowMoreButton = styled.button`
    background: none;
    border: none;
    color: #027b8b;
    cursor: pointer;
    margin-bottom: 20px;
`;

const NavButton = styled.button<{ disabled?: boolean }>`
    background-color: ${({ disabled }) => (disabled ? '#ccc' : '#027b8b')};
    color: #fff;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: ${({ disabled }) => (disabled ? 'not-allowed' : 'pointer')};
    &:hover {
        background-color: ${({ disabled }) => (disabled ? '#ccc' : '#025e6b')};
    }
`;
