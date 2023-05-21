import { Injectable } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RoleService {
  constructor(private auth: AuthService) {}

  async getUserRole(): Promise<string | undefined> {
    try {
      const claims = await firstValueFrom(this.auth.idTokenClaims$);
      return claims?.['http://localhost:4200/roles'];
    } catch (error) {
      console.error('Error retrieving user role:', error);
      return undefined;
    }
  }
}
