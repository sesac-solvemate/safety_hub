import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const DetailTypeForm: React.FC = () => {
    const [riskFactors, setRiskFactors] = useState<string[]>([]);
    const [recommendedFactors, setRecommendedFactors] = useState<string[]>([]);
    const [newRiskFactor, setNewRiskFactor] = useState('');
    const [additionalNotes, setAdditionalNotes] = useState('');
    const [emergencyEquipments, setEmergencyEquipments] = useState<string[]>([]);
    const [selectedEquipment, setSelectedEquipment] = useState('');
    const [emergencyNotes, setEmergencyNotes] = useState('');
    const [emergencyContacts, setEmergencyContacts] = useState<{ name: string, phone: string, notes: string }[]>([]);
    const [newContact, setNewContact] = useState({ name: '', phone: '', notes: '' });
    const [file, setFile] = useState<File | null>(null);

    useEffect(() => {
        axios.get('/api/risk-factors')
            .then(response => setRiskFactors(response.data))
            .catch(error => console.error(error));

        axios.get('/api/recommended-factors')
            .then(response => setRecommendedFactors(response.data))
            .catch(error => console.error(error));

        axios.get('/api/emergency-equipments')
            .then(response => setEmergencyEquipments(response.data))
            .catch(error => console.error(error));
    }, []);

    const handleAddRiskFactor = () => {
        if (newRiskFactor.trim() !== '') {
            setRiskFactors([...riskFactors, newRiskFactor]);
            setNewRiskFactor(''); // Clear the input field
        }
    };

    const handleRemoveRiskFactor = (index: number) => {
        setRiskFactors(riskFactors.filter((_, i) => i !== index));
    };

    const handleAddEmergencyContact = () => {
        setEmergencyContacts([...emergencyContacts, newContact]);
        setNewContact({ name: '', phone: '', notes: '' });
    };

    const handleRemoveEmergencyContact = (index: number) => {
        setEmergencyContacts(emergencyContacts.filter((_, i) => i !== index));
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    return (
        <FormContainer>
            <Section>
                <SectionTitle>위험요인</SectionTitle>
                <Description>4-5개의 위험요인이 10분 안전자료에 적합합니다.</Description>
                <Divider />
                <RiskList>
                    {riskFactors.map((factor, index) => (
                        <RiskItem key={index}>
                            <RemoveButton onClick={() => handleRemoveRiskFactor(index)}>−</RemoveButton>
                            {factor}
                        </RiskItem>
                    ))}
                </RiskList>
                <AddRiskFactor>
                    <AddRiskInput
                        type="text"
                        placeholder="위험요인 추가하기"
                        value={newRiskFactor}
                        onChange={(e) => setNewRiskFactor(e.target.value)}
                    />
                    <AddButton onClick={handleAddRiskFactor}>+ 추가하기</AddButton>
                </AddRiskFactor>
                <RecommendationTitle>추천 위험요인</RecommendationTitle>
                <Divider />
                <RecommendationList>
                    {recommendedFactors.map((factor, index) => (
                        <RecommendationItem key={index}>{factor}</RecommendationItem>
                    ))}
                </RecommendationList>
            </Section>

            <Section>
                <SectionTitle>추가 당부사항</SectionTitle>
                <TextArea
                    placeholder="안전을 위해 특히 당부하시고 싶은 사항을 입력해주세요."
                    value={additionalNotes}
                    onChange={(e) => setAdditionalNotes(e.target.value)}
                />
            </Section>

            <Section>
                <SectionTitle>비상상황시 필요 정보</SectionTitle>
                <Divider />
                <Select
                    value={selectedEquipment}
                    onChange={(e) => setSelectedEquipment(e.target.value)}
                >
                    <option value="">비상장비 선택하기</option>
                    {emergencyEquipments.map((equipment, index) => (
                        <option key={index} value={equipment}>{equipment}</option>
                    ))}
                </Select>
                <TextArea
                    placeholder="비상장비의 위치 및 기타 필요사항을 적어주세요."
                    value={emergencyNotes}
                    onChange={(e) => setEmergencyNotes(e.target.value)}
                />
            </Section>

            <Section>
                <SectionTitle>비상연락망</SectionTitle>
                <Divider />
                <EmergencyContactList>
                    {emergencyContacts.map((contact, index) => (
                        <EmergencyContactItem key={index}>
                            <ContactInfo>{contact.name}</ContactInfo>
                            <ContactInfo>{contact.phone}</ContactInfo>
                            <ContactInfo>{contact.notes}</ContactInfo>
                            <RemoveButton onClick={() => handleRemoveEmergencyContact(index)}>−</RemoveButton>
                        </EmergencyContactItem>
                    ))}
                </EmergencyContactList>
                <EmergencyContactForm>
                    <ContactInput
                        type="text"
                        placeholder="이름"
                        value={newContact.name}
                        onChange={(e) => setNewContact({ ...newContact, name: e.target.value })}
                    />
                    <ContactInput
                        type="text"
                        placeholder="연락처"
                        value={newContact.phone}
                        onChange={(e) => setNewContact({ ...newContact, phone: e.target.value })}
                    />
                    <ContactInput
                        type="text"
                        placeholder="특이사항"
                        value={newContact.notes}
                        onChange={(e) => setNewContact({ ...newContact, notes: e.target.value })}
                    />
                    <AddButton onClick={handleAddEmergencyContact}>+</AddButton>
                </EmergencyContactForm>
            </Section>

            <Section>
                <SectionTitle>도면</SectionTitle>
                <Description>비상구, 소화기, AED 위치 등이 표시되어있는 도면을 첨부해주세요.</Description>
                <FileInput type="file" onChange={handleFileChange} />
            </Section>
        </FormContainer>
    );
};

export default DetailTypeForm;

const FormContainer = styled.div`
    width: 85%;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: flex-start;
    padding: 30px 0px;
    align-items: flex-start;
    & > * {
        width: 100%;
        margin-bottom: 20px;
    }
`;

const Section = styled.div`
    display: flex;
    flex-direction: column;
`;

const SectionTitle = styled.h2`
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 5px;
    text-align: left;
`;

const Description = styled.p`
    font-size: 14px;
    color: #757575;
    margin-top: 0px;
    margin-bottom: 10px;
    text-align: left;
`;

const RiskList = styled.ul`
    list-style: none;
    padding: 0;
    margin: 0;
    font-family: NotoSansKR-Regular;
`;

const RiskItem = styled.li`
    display: flex;
    align-items: center;
    margin-bottom: 10px;
`;

const RemoveButton = styled.button`
    background: none;
    border: none;
    color: red;
    cursor: pointer;
    margin-right: 10px;
`;

const AddRiskFactor = styled.div`
    display: flex;
    align-items: center;
    margin-top: 10px;
    width: 100%;
`;

const AddRiskInput = styled.input`
    flex-grow: 1;
    height: 40px;
    font-size: 16px;
    padding: 8px;
    font-family: NotoSansKR-Regular;
    border: 1px solid #ddd;
    border-radius: 4px;
`;

const AddButton = styled.button`
    background-color: #027b8b;
    color: #fff;
    padding: 10px;
    font-size: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 10px;
    height: 40px;
    font-size: 16px;
    font-family: NotoSansKR-Regular;
    &:hover {
        background-color: #025e6b;
    }
`;

const RecommendationTitle = styled.h3`
    font-size: 16px;
    font-family: NotoSansKR-SemiBold;
    padding-top: 5px;
    padding-left: 10px;
    text-align: left;
    margin-bottom: 3px;
`;

const RecommendationList = styled.ul`
    list-style: none;
    padding: 0;
    margin: 0;
    text-align: left;
`;

const RecommendationItem = styled.li`
    margin-bottom: 10px;
    cursor: pointer;
    text-align: left;
`;

const TextArea = styled.textarea`
    width: 100%;
    height: 40px;
    padding: 8px;
    font-size: 16px;
    font-family: NotoSansKR-Regular;
    border: 1px solid #ddd;
    border-radius: 4px;
`;

const Select = styled.select`
    width: 100%;
    height: 40px;
    padding: 8px;
    font-size: 16px;
    font-family: NotoSansKR-Regular;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 10px;
`;

const EmergencyContactList = styled.ul`
    list-style: none;
    padding: 0;
    margin: 0;
    text-align: left;
`;

const EmergencyContactItem = styled.li`
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
`;


const ContactInfo = styled.span`
    width: 30%;
`;

const EmergencyContactForm = styled.div`
    display: flex;
    align-items: center;
    margin-top: 10px;
`;

const ContactInput = styled.input`
    width: 30%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
`;

const FileInput = styled.input`
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
`;

const Divider = styled.hr`
    width: 100%;
    border: 0;
    height: 1px;
    background: #ddd;
    margin-bottom: 10px;
    padding: 0;
`;