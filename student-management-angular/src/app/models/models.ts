interface User {
  name: string;
  given_name: string;
  email: string;
}

export interface Student {
  id: number;
  name: string;
  nickname: string;
  grade: string;
  email: string;
  profilePicture: string;
  user: User;
  // additional properties as needed
}

interface Instructor {
  id: string;
  user: User;
}


export interface Course {
  id: number;
  name: string;
  instructor: Instructor;
}

export interface Enrollment {
  course_id: number,
  course_name: string;
  student: Student;
  grade: string;
}
