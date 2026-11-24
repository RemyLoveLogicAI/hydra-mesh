//
// HydraCockpitView.swift
// HYDRA-MESH iOS & iMessage Companion View
// Production SwiftUI Component for iPhone, iPad, and Live Activities
//

import SwiftUI

public struct HydraAgent: Identifiable {
    public let id: String
    public let name: String
    public let role: String
    public let channel: String
    public let status: String
    public let tint: Color
}

public struct HydraCockpitView: View {
    @State private var pulseAnimation = false
    @State private var skepticScore: Int = 90
    
    let agents: [HydraAgent] = [
        HydraAgent(id: "1", name: "DevTheDude", role: "Architect", channel: "TUI / Local", status: "Active", tint: .teal),
        HydraAgent(id: "2", name: "Telegram Bot", role: "Mobile Ingress", channel: "Telegram", status: "Connected", tint: .blue),
        HydraAgent(id: "3", name: "Slack Bot", role: "Team Canvas", channel: "Slack", status: "Connected", tint: .pink),
        HydraAgent(id: "4", name: "Discord Bot", role: "Community Hub", channel: "Discord", status: "Connected", tint: .purple),
        HydraAgent(id: "5", name: "Hermes (Claw)", role: "Autonomous Agent", channel: "OpenBot", status: "Standby", tint: .orange)
    ]
    
    public init() {}
    
    public var body: some View {
        NavigationStack {
            ZStack {
                Color(red: 0.03, green: 0.04, blue: 0.07).ignoresSafeArea()
                
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Header / Quorum Badge
                        HStack {
                            VStack(alignment: .leading) {
                                Text("HYDRA-MESH")
                                    .font(.system(.title, design: .monospaced, weight: .bold))
                                    .foregroundColor(.cyan)
                                Text("2027 Agent Swarm Cockpit")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                            HStack(spacing: 6) {
                                Circle()
                                    .fill(Color.green)
                                    .frame(width: 8, height: 8)
                                    .scaleEffect(pulseAnimation ? 1.3 : 1.0)
                                    .animation(.easeInOut(duration: 1.0).repeatForever(), value: pulseAnimation)
                                Text("MESH LIVE")
                                    .font(.caption2.bold())
                                    .foregroundColor(.green)
                            }
                            .padding(.horizontal, 10)
                            .padding(.vertical, 6)
                            .background(Color.green.opacity(0.12))
                            .clipShape(Capsule())
                        }
                        
                        // Skeptic Reality Meter Card
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Label("GROKBOT SKEPTIC SCORE", systemImage: "shield.checkerboard")
                                    .font(.caption.bold())
                                    .foregroundColor(.yellow)
                                Spacer()
                                Text("\(skepticScore)/100")
                                    .font(.system(.headline, design: .monospaced, weight: .bold))
                                    .foregroundColor(.green)
                            }
                            
                            ProgressView(value: Double(skepticScore), total: 100)
                                .tint(.green)
                            
                            Text("Port Hygiene: 100% clean • Quorum: 6 Agents • TypeFire Vault: Mounted")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .background(RoundedRectangle(cornerRadius: 14).fill(Color.white.opacity(0.05)))
                        .overlay(RoundedRectangle(cornerRadius: 14).stroke(Color.white.opacity(0.1), lineWidth: 1))
                        
                        // Active Channels
                        Text("ACTIVE AGENT FLEET")
                            .font(.caption.bold())
                            .foregroundColor(.cyan)
                        
                        ForEach(agents) { agent in
                            HStack(spacing: 14) {
                                Circle()
                                    .fill(agent.tint)
                                    .frame(width: 12, height: 12)
                                
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(agent.name)
                                        .font(.subheadline.bold())
                                        .foregroundColor(.white)
                                    Text("\(agent.role) • \(agent.channel)")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                }
                                Spacer()
                                Text(agent.status)
                                    .font(.caption2.bold())
                                    .foregroundColor(agent.tint)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(agent.tint.opacity(0.15))
                                    .clipShape(Capsule())
                            }
                            .padding()
                            .background(RoundedRectangle(cornerRadius: 12).fill(Color.white.opacity(0.03)))
                        }
                    }
                    .padding()
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .onAppear {
                pulseAnimation = true
            }
        }
    }
}
