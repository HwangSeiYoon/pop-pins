from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import json
from datetime import datetime
import os

app = FastAPI(title="학습 계획 생성 API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델 정의
class LearningPlanRequest(BaseModel):
    title: str = Field(..., description="학습 계획 제목", min_length=1)
    goal: str = Field(..., description="학습 목표/주제", min_length=1)
    startDate: str = Field(..., description="시작일 (YYYY-MM-DD 형식)")
    endDate: str = Field(..., description="종료일 (YYYY-MM-DD 형식)")
    maxCourseCount: Optional[int] = Field(None, description="최대 학습 과정 갯수 (AI에게 맡기기면 null)")
    currentStatus: Optional[str] = Field(None, description="현재 학습 상황")
    requests: Optional[str] = Field(None, description="요청 사항")
    referenceLinks: Optional[List[str]] = Field(None, description="참고 링크 목록")

    @field_validator('startDate', 'endDate')
    @classmethod
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('날짜 형식이 올바르지 않습니다. (YYYY-MM-DD 형식)')

    @field_validator('maxCourseCount')
    @classmethod
    def validate_course_count(cls, v):
        if v is not None and v < 1:
            raise ValueError('최대 학습 과정 갯수는 1 이상이어야 합니다.')
        return v

    def validate_dates(self):
        """시작일과 종료일의 유효성 검증"""
        start_date = datetime.strptime(self.startDate, '%Y-%m-%d')
        end_date = datetime.strptime(self.endDate, '%Y-%m-%d')
        
        if start_date > end_date:
            raise ValueError('시작일은 종료일보다 이전이어야 합니다.')

class LearningPlanResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class HealthResponse(BaseModel):
    status: str
    message: str

def save_json_to_file(data: dict):
    """
    JSON 데이터를 파일로 저장하는 함수
    """
    try:
        # 타임스탬프 추가
        data_with_timestamp = {
            'createdAt': datetime.now().isoformat(),
            **data
        }
        
        # 파일명 생성 (타임스탬프 기반)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'learning_plan_{timestamp}.json'
        
        # data 디렉토리 경로 (현재 파일 기준 상대 경로)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        filepath = os.path.join(data_dir, filename)
        
        # JSON 파일로 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_with_timestamp, f, ensure_ascii=False, indent=2)
        
        print(f'JSON 파일 저장 완료: {filepath}')
        
    except Exception as e:
        print(f'JSON 파일 저장 중 오류 발생: {str(e)}')

@app.post('/api/learning-plan', response_model=LearningPlanResponse)
async def create_learning_plan(request_data: LearningPlanRequest):
    """
    학습 계획 생성 API 엔드포인트
    JSON 데이터를 받아서 처리합니다.
    """
    try:
        # 날짜 유효성 검증
        request_data.validate_dates()
        
        # Pydantic 모델을 dict로 변환
        data = request_data.model_dump()
        
        # JSON 파일로 저장 (선택사항)
        # 실제 프로젝트에서는 데이터베이스에 저장하거나 AI API를 호출할 수 있습니다.
        save_json_to_file(data)
        
        # 응답 반환
        return LearningPlanResponse(
            success=True,
            message='학습 계획이 성공적으로 생성되었습니다.',
            data=data
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'서버 오류가 발생했습니다: {str(e)}')

@app.get('/api/health', response_model=HealthResponse)
async def health_check():
    """
    서버 상태 확인 엔드포인트
    """
    return HealthResponse(
        status='healthy',
        message='서버가 정상적으로 실행 중입니다.'
    )

if __name__ == '__main__':
    import uvicorn
    
    print('=' * 50)
    print('학습 계획 생성 API 서버 시작')
    print('=' * 50)
    print('API 엔드포인트:')
    print('  POST /api/learning-plan - 학습 계획 생성')
    print('  GET  /api/health - 서버 상태 확인')
    print('  GET  /docs - Swagger UI 문서')
    print('  GET  /redoc - ReDoc 문서')
    print('=' * 50)
    
    uvicorn.run(app, host='0.0.0.0', port=5000, reload=True)
