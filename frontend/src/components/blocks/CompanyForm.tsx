import React, { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import businessIcon from '../../assets/images/apartment.svg';
import industryIcon from '../../assets/images/folder.svg';
import reportIcon from '../../assets/images/content.svg';
import industryData from '../../assets/industry.json'; // Ensure this path is correct

interface Industry {
    code: number;
    name: string;
    midCategory: MidCategory[];
}

interface MidCategory {
    code: number;
    name: string;
    subCategory: SubCategory[];
}

interface SubCategory {
    code: number;
    name: string;
}

const CompanyForm: React.FC = () => {
    const [formData, setFormData] = useState({
        companyName: '',
        industry: '',
        reportFile: null as File | null,
    });
    const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);
    const [selectedMidCategory, setSelectedMidCategory] = useState<MidCategory | null>(null);
    const [selectedSubCategory, setSelectedSubCategory] = useState<SubCategory | null>(null);
    const [isIndustrySelectorOpen, setIsIndustrySelectorOpen] = useState(false);
    
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, files } = e.target;
        if (name === 'reportFile' && files) {
            setFormData({ ...formData, [name]: files[0] });
        } else {
            setFormData({ ...formData, [name]: value });
        }
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const submitData = new FormData();
        submitData.append('companyName', formData.companyName);
        submitData.append('industry', formData.industry);
        if (formData.reportFile) {
            submitData.append('reportFile', formData.reportFile);
        }

        // Here would be the axios call to the backend
        // axios.post('/api/submit', submitData, { headers: { 'Content-Type': 'multipart/form-data' } })
        //     .then(() => {
        //         navigate('/firstForm');
        //     });

        // Simulate successful form submission and redirect
        console.log('Form submitted:', Object.fromEntries(submitData.entries()));
        navigate('/firstForm');
    };

    const handleIndustrySelection = (industry: Industry) => {
        setSelectedIndustry(industry);
        setSelectedMidCategory(null);
        setSelectedSubCategory(null);
    };

    const handleMidCategorySelection = (midCategory: MidCategory) => {
        setSelectedMidCategory(midCategory);
        setSelectedSubCategory(null);
    };

    const handleSubCategorySelection = (subCategory: SubCategory) => {
        setSelectedSubCategory(subCategory);
        setFormData({ ...formData, industry: subCategory.name });
        setIsIndustrySelectorOpen(false);
    };

    const handleReset = () => {
        setFormData({
            companyName: '',
            industry: '',
            reportFile: null,
        });
        setSelectedIndustry(null);
        setSelectedMidCategory(null);
        setSelectedSubCategory(null);
    };

    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormRow>
                <Icon src={businessIcon} alt="business icon" />
                <FormLabel>사업장명*</FormLabel>
            </FormRow>
            <FormInput
                type="text"
                name="companyName"
                placeholder="사업장명을 입력하세요"
                value={formData.companyName}
                onChange={handleChange}
                required
            />
            <FormRow>
                <Icon src={industryIcon} alt="industry icon" />
                <FormLabel>업종명*</FormLabel>
                <ResetButton type="button" onClick={handleReset}>
                    초기화하기
                </ResetButton>
            </FormRow>
            <FormInput
                type="text"
                name="industry"
                placeholder="업종을 선택하세요"
                value={formData.industry}
                onClick={() => setIsIndustrySelectorOpen(!isIndustrySelectorOpen)}
                readOnly
                required
            />
            {isIndustrySelectorOpen && (
                <IndustrySelector>
                    <IndustryList>
                        <CategoryColumn>
                            <CategoryTitle>대분류</CategoryTitle>
                            {industryData.map((industry) => (
                                <IndustryOption key={industry.code} onClick={() => handleIndustrySelection(industry)}>
                                    {industry.name}
                                </IndustryOption>
                            ))}
                        </CategoryColumn>
                        {selectedIndustry && selectedIndustry.midCategory && (
                            <CategoryColumn>
                                <CategoryTitle>중분류</CategoryTitle>
                                {selectedIndustry.midCategory.map((midCategory) => (
                                    <IndustryOption key={midCategory.code} onClick={() => handleMidCategorySelection(midCategory)}>
                                        {midCategory.name}
                                    </IndustryOption>
                                ))}
                            </CategoryColumn>
                        )}
                        {selectedMidCategory && selectedMidCategory.subCategory && (
                            <CategoryColumn>
                                <CategoryTitle>소분류</CategoryTitle>
                                {selectedMidCategory.subCategory.map((subCategory) => (
                                    <IndustryOption key={subCategory.code} onClick={() => handleSubCategorySelection(subCategory)}>
                                        {subCategory.name}
                                    </IndustryOption>
                                ))}
                            </CategoryColumn>
                        )}
                    </IndustryList>
                    <ConfirmButton type="button" onClick={() => setIsIndustrySelectorOpen(false)}>
                        확인
                    </ConfirmButton>
                </IndustrySelector>
            )}
            <FormRow>
                <Icon src={reportIcon} alt="report icon" />
                <FormLabel>가장 최근에 작성한 위험성 평가보고서를 첨부해 주세요. (선택)</FormLabel>
            </FormRow>
            <FormInput
                type="file"
                name="reportFile"
                onChange={handleChange}
            />
            <SubmitButton type="submit">다음으로</SubmitButton>
        </FormContainer>
    );
};

export default CompanyForm;

const FormContainer = styled.form`
    width: 85%;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: flex-start;
    padding: 30px 0px;
    align-items: center;
`;

const FormRow = styled.div`
    width: 100%;
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    flex-direction: row;
`;

const Icon = styled.img`
    width: 24px;
    height: 24px;
    margin-right: 2px;
`;

const FormLabel = styled.label`
    font-size: 16px;
    font-weight: bold;
    color: #333;
    flex-grow: 1;
    margin-left: 4px;
    text-align: left;
`;

const FormInput = styled.input`
    width: 100%;
    height: 30px;
    font-size: 24px;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 20px;
`;

const ResetButton = styled.button`
    background-color: none;
    align-items: center;
    color: #000;
    border: none;
    border-radius: 4px;
    padding: 10px;
    cursor: pointer;
    margin-left: 10px;

    &:hover {
        text-decoration: underline;
    }
`;

const IndustrySelector = styled.div`
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 20px;
    width: 100%;
`;

const IndustryList = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
`;

const CategoryColumn = styled.div`
    flex: 1;
    overflow-y: auto;
    margin-right: 10px;
`;

const CategoryTitle = styled.h3`
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
`;

const IndustryOption = styled.div`
    padding: 8px;
    cursor: pointer;
    &:hover {
        background-color: #f0f0f0;
    }
`;

const ConfirmButton = styled.button`
    background-color: #027b8b;
    color: #fff;
    padding: 10px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    align-self: flex-end;

    &:hover {
        background-color: #025e6b;
    }
`;

const SubmitButton = styled.button`
    background-color: #027b8b;
    color: #fff;
    padding: 15px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    align-self: flex-end;

    &:hover {
        background-color: #025e6b;
    }
`;

