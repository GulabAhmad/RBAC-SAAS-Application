from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime


# Base schemas
class OrganizationBase(BaseModel):
    name: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class RoleBase(BaseModel):
    name: str


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None


# Create schemas
class OrganizationCreate(OrganizationBase):
    pass


class UserCreate(UserBase):
    password: str
    organization_name: str  # For creating organization during registration


class UserRegister(UserBase):
    password: str
    confirm_password: str
    organization_name: str


class RoleCreate(RoleBase):
    organization_id: int


class PermissionCreate(PermissionBase):
    pass


# Response schemas
class Organization(OrganizationBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Permission(PermissionBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class Role(RoleBase):
    id: int
    organization_id: int
    created_at: datetime
    permissions: List[Permission] = []
    
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    organization_id: int
    role_id: int
    is_email_verified: bool
    created_at: datetime
    organization: Organization
    role: Role
    
    model_config = ConfigDict(from_attributes=True)


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    email: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class EmailVerification(BaseModel):
    email: EmailStr
    verification_code: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str
    confirm_password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetVerify(BaseModel):
    email: EmailStr
    reset_code: str


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str
    confirm_password: str


# Role-Permission schemas
class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int


class RolePermissionResponse(BaseModel):
    role_id: int
    permission_id: int
    role: Role
    permission: Permission
    
    model_config = ConfigDict(from_attributes=True)
