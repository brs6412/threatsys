import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrls: ['./home.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    RouterLink
  ]
})
export class Home implements OnInit {
  userCount = 0;
  iocCount = 0;
  loading = true;

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.loading = true;

    this.apiService.getUsers().subscribe({
      next: (users) => {
        this.userCount = users.length;
        this.checkLoadingComplete();
      },
      error: (error) => {
        console.error('Error loading users:', error);
        this.checkLoadingComplete();
      }
    });

    this.apiService.getIOCs().subscribe({
      next: (iocs) => {
        this.iocCount = iocs.length;
        this.checkLoadingComplete();
      },
      error: (error) => {
        console.error('Error loading IOCs:', error);
        this.checkLoadingComplete();
      }
    });
  }

  private checkLoadingComplete() {
    // Simple loading state management
    setTimeout(() => {
      this.loading = false;
    }, 500);
  }
}