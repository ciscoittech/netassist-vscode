/**
 * SanitizationProvider - Core IP/credential sanitization functionality
 * This is the secret sauce that enables secure AI assistance
 */

import * as vscode from 'vscode';
import axios, { AxiosInstance } from 'axios';
import { ConfigurationManager } from '../core/ConfigurationManager';

export interface SanitizationRequest {
    text: string;
    session_id?: string;
}

export interface SanitizationResponse {
    sanitized_text: string;
    session_id: string;
    entity_count: number;
    confidence: number;
    mapping_id: string;
}

export interface RestorationRequest {
    text: string;
    session_id: string;
}

export interface RestorationResponse {
    restored_text: string;
    entity_count: number;
    success: boolean;
}

export interface NetworkEntity {
    type: string;
    original: string;
    sanitized: string;
    confidence: number;
}

export class SanitizationProvider {
    private httpClient: AxiosInstance;
    private serverUrl: string;
    private currentSessionId: string | null = null;
    private auditLog: SanitizationAudit[] = [];

    constructor(private configManager: ConfigurationManager) {
        this.serverUrl = this.configManager.getSanitizationServerUrl();
        this.httpClient = axios.create({
            baseURL: this.serverUrl,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Listen for configuration changes
        vscode.workspace.onDidChangeConfiguration(event => {
            if (event.affectsConfiguration('netassist.sanitizationServer')) {
                this.serverUrl = this.configManager.getSanitizationServerUrl();
                this.httpClient.defaults.baseURL = this.serverUrl;
            }
        });
    }

    /**
     * Check if sanitization server is healthy
     */
    async checkServerHealth(): Promise<boolean> {
        try {
            const response = await this.httpClient.get('/api/health');
            return response.status === 200;
        } catch (error) {
            console.error('Sanitization server health check failed:', error);
            return false;
        }
    }

    /**
     * Sanitize network configuration text
     */
    async sanitize(text: string, sessionId?: string): Promise<SanitizationResponse> {
        try {
            const request: SanitizationRequest = {
                text,
                session_id: sessionId || this.currentSessionId || undefined
            };

            const response = await this.httpClient.post<SanitizationResponse>('/api/sanitize', request);
            const result = response.data;

            // Update current session ID
            this.currentSessionId = result.session_id;

            // Log sanitization for audit
            if (this.configManager.isAuditLogEnabled()) {
                this.auditLog.push({
                    timestamp: new Date(),
                    action: 'sanitize',
                    sessionId: result.session_id,
                    entityCount: result.entity_count,
                    confidence: result.confidence,
                    originalHash: this.hashText(text),
                    sanitizedHash: this.hashText(result.sanitized_text)
                });
            }

            return result;
        } catch (error) {
            const message = axios.isAxiosError(error)
                ? `Sanitization server error: ${error.response?.data?.detail || error.message}`
                : `Sanitization failed: ${error}`;

            throw new Error(message);
        }
    }

    /**
     * Restore original values from sanitized text
     */
    async restore(text: string, sessionId?: string): Promise<RestorationResponse> {
        try {
            const request: RestorationRequest = {
                text,
                session_id: sessionId || this.currentSessionId || ''
            };

            if (!request.session_id) {
                throw new Error('No session ID available for restoration');
            }

            const response = await this.httpClient.post<RestorationResponse>('/api/restore', request);
            const result = response.data;

            // Log restoration for audit
            if (this.configManager.isAuditLogEnabled()) {
                this.auditLog.push({
                    timestamp: new Date(),
                    action: 'restore',
                    sessionId: request.session_id,
                    entityCount: result.entity_count,
                    confidence: 1.0,
                    originalHash: this.hashText(text),
                    sanitizedHash: this.hashText(result.restored_text)
                });
            }

            return result;
        } catch (error) {
            const message = axios.isAxiosError(error)
                ? `Restoration server error: ${error.response?.data?.detail || error.message}`
                : `Restoration failed: ${error}`;

            throw new Error(message);
        }
    }

    /**
     * Process text through complete sanitize -> AI -> restore cycle
     */
    async processThroughAI(
        text: string,
        aiProcessor: (sanitizedText: string) => Promise<string>
    ): Promise<string> {
        // Step 1: Sanitize
        const sanitizeResult = await this.sanitize(text);

        try {
            // Step 2: Process with AI
            const aiResponse = await aiProcessor(sanitizeResult.sanitized_text);

            // Step 3: Restore original values
            const restoreResult = await this.restore(aiResponse, sanitizeResult.session_id);

            return restoreResult.restored_text;
        } catch (error) {
            // If AI processing fails, we still want to clean up the session
            await this.clearSession(sanitizeResult.session_id);
            throw error;
        }
    }

    /**
     * Detect network entities without sanitization (for preview)
     */
    async detectEntities(text: string): Promise<NetworkEntity[]> {
        try {
            // This would require an additional endpoint on the server
            const response = await this.httpClient.post('/api/detect', { text });
            return response.data.entities;
        } catch (error) {
            console.error('Entity detection failed:', error);
            return [];
        }
    }

    /**
     * Get session information
     */
    async getSessionInfo(sessionId?: string): Promise<any> {
        try {
            const id = sessionId || this.currentSessionId;
            if (!id) {
                throw new Error('No session ID available');
            }

            const response = await this.httpClient.get(`/api/sessions/${id}`);
            return response.data;
        } catch (error) {
            console.error('Failed to get session info:', error);
            return null;
        }
    }

    /**
     * Clear current session
     */
    async clearSession(sessionId?: string): Promise<void> {
        try {
            const id = sessionId || this.currentSessionId;
            if (!id) {
                return;
            }

            await this.httpClient.delete(`/api/sessions/${id}`);

            if (id === this.currentSessionId) {
                this.currentSessionId = null;
            }
        } catch (error) {
            console.error('Failed to clear session:', error);
        }
    }

    /**
     * Create new session
     */
    createNewSession(): void {
        this.currentSessionId = null;
    }

    /**
     * Get current session ID
     */
    getCurrentSessionId(): string | null {
        return this.currentSessionId;
    }

    /**
     * Get audit log
     */
    getAuditLog(): SanitizationAudit[] {
        return [...this.auditLog];
    }

    /**
     * Export audit log
     */
    async exportAuditLog(): Promise<void> {
        if (this.auditLog.length === 0) {
            vscode.window.showInformationMessage('No audit log entries to export');
            return;
        }

        const content = JSON.stringify(this.auditLog, null, 2);
        const document = await vscode.workspace.openTextDocument({
            content,
            language: 'json'
        });

        await vscode.window.showTextDocument(document);
    }

    /**
     * Get sanitization statistics
     */
    getStatistics(): SanitizationStats {
        const totalOperations = this.auditLog.length;
        const sanitizeOps = this.auditLog.filter(entry => entry.action === 'sanitize').length;
        const restoreOps = this.auditLog.filter(entry => entry.action === 'restore').length;
        const totalEntities = this.auditLog.reduce((sum, entry) => sum + entry.entityCount, 0);
        const avgConfidence = this.auditLog.length > 0
            ? this.auditLog.reduce((sum, entry) => sum + entry.confidence, 0) / this.auditLog.length
            : 0;

        return {
            totalOperations,
            sanitizeOperations: sanitizeOps,
            restoreOperations: restoreOps,
            totalEntitiesProcessed: totalEntities,
            averageConfidence: avgConfidence,
            sessionsCreated: new Set(this.auditLog.map(entry => entry.sessionId)).size
        };
    }

    /**
     * Hash text for audit logging (without storing actual content)
     */
    private hashText(text: string): string {
        // Simple hash for audit purposes (not cryptographically secure)
        let hash = 0;
        for (let i = 0; i < text.length; i++) {
            const char = text.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return hash.toString(16);
    }

    /**
     * Dispose resources
     */
    dispose(): void {
        // Clear current session on shutdown
        if (this.currentSessionId) {
            this.clearSession().catch(console.error);
        }
    }
}

interface SanitizationAudit {
    timestamp: Date;
    action: 'sanitize' | 'restore';
    sessionId: string;
    entityCount: number;
    confidence: number;
    originalHash: string;
    sanitizedHash: string;
}

interface SanitizationStats {
    totalOperations: number;
    sanitizeOperations: number;
    restoreOperations: number;
    totalEntitiesProcessed: number;
    averageConfidence: number;
    sessionsCreated: number;
}